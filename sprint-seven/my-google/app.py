# Python standard libraries
import json
import os
import sqlite3

# Third party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:        return (
            "<h2  style='color:pink;'> Hello, {}, you're logged in!<br> Email: {}</h2>"
	"<h2 style='color:pink;'>This website  was created for CS4320</h2>"
"<h1 style='color:blue;'>Sarina's Book Blog<h1>"
"<p>My name is Sarina Gaines and I am a junior at the Unversity of Missouri. I am an avid reader and created this page for other's to view my book reccomendations. On this page, you will find various books I enjoy reading as well as reviews to these books in case you are wanting to learn more about the book. Feel free to contact me with any of your own reccomendations so that I may read them myself!</p>"
"<h3 style='color:green;'>Books I reccomend:</h3>"
"<ul style='color:green;'><li>Harry Potter and the Sorcerer's Stone, by J. K. Rowling</li><li>Outlander, by Diana Gabaldon</li><li>Gone with the Wind, by Margaret Mitchell</li><li>The Catcher in the Rye, by J.D. Salinger</li><li>Dead Until Dark, by Charlaine Harris</li><li>A Song of Ice and Fire, by George R. R. Martin</li><li>The Hobbit, by J. R. R. Tolkien</li><li>Flowers for Algernon, by Daniel Keyes</li><li>Jane Eyre, by Charlotte Bronte</li><li>To Kill A Mockingbird, by Harper Lee</li><li>The Chronicles of Narnia, by C. S. Lewis</li></ul>"
"<h3 style='color:blue;'>Book Reviews</h3>"
"<a href= 'https://www.goodreads.com/book/show/10964.Outlander'> Outlander Book Review</a><br>"
"<a href= 'https://www.goodreads.com/book/show/5107.The_Catcher_in_the_Rye'> The Catcher in the Rye Book Review</a><br>"
"<a href = 'https://www.goodreads.com/book/show/3.Harry_Potter_and_the_Sorcerer_s_Stone'> Harry Potter and the Sorcerer's Stone Book Review</a><br>"
"<a href = 'https://www.goodreads.com/book/show/18405.Gone_with_the_Wind'> Gone with the Wind Book Review</a><br>"
"<a href= 'https://www.goodreads.com/book/show/9814682-a-song-of-ice-and-fire'> A Song of Ice and Fire Book Review</a><br>"
"<h2>Send me a book YOU reccomend:</h2>"
"<form action='mailto:sgfx8@mail.missouri.edu' method='post' enctype='text/plain'>Name:<br><input type='text' name='name'><br>E-mail:<br><input type='text' name='mail'><br>Reccommendation:<br><input type='text' name='reccommendation' size='50'><br><br><input type='submit' value='Send'><input type='reset' value='Reset'></form>"
 "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic" height="42" width="42"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
