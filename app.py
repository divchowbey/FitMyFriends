from flask import Flask, render_template, redirect, flash, request, url_for
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
import json
import os
import sqlite3
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

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
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

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
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


DEGREE = [('1', "Middle School"), ('2', "High School"), ('3', "College Student"), ('4', "Grad School")]
class MatchForm(Form):
    name = StringField('Name', [validators.optional(), validators.length(max=200)])
    email = StringField('Email Address', [validators.optional(), validators.length(max=200)])
    degree = SelectField(label='Degee', choices=DEGREE)
    skills = StringField('Skills', [validators.optional(), validators.length(max=200)])
    otherinterests = StringField('Other Interests', [validators.optional(), validators.length(max=200)])

@app.route('/Statistics')
def statis():
    return render_template('statistics.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/inspiration')
def inspiration():
    return render_template('inspiration.html')
@app.route('/fit', methods=['GET', 'POST'])
def fit():
    form = MatchForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        degree = form.degree.data
        skills = form.skills.data
        otherinterests = form.otherinterests.data
        jsonFile = convertJson(name, email, degree, skills, otherinterests)
        output = "software engineer"

        if "programming" or "Programming" in skills:
            output = "software engineer"
        if "communication" in skills:
            output = "Product Manager, Recruiter"
        if "Communication" in skills:
            output = "Product Manager, Recruiter"
        if "Design" in skills:
            output = "UI/UX"
        if "design" in skills:
            output = "UI/UX"
        if "Gaming" in skills:
            output = "Game Designer"
        if "gaming" in skills:
            output = "Game Designer"
        if "Leadership" in skills:
            output = "Project Manager"

        if "leadership" in skills:
            output = "Project Manager"

        return render_template('displayresult.html', companies = output)

    return render_template('fit.html', form=form)

def convertJson(name, email, degree, skills, otherinterests):
    result = []
    myjson = {
            'Name': name,
            'Email': email,
            'Degree': degree,
            'Skills': skills,
            'Interests': otherinterests
    }
    result.append(myjson)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(ssl_context="adhoc")
    # app.run(debug=True)
