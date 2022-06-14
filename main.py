from flask import Flask, redirect, url_for
from authlib.integrations.flask_client import OAuth

import settings


app = Flask(__name__)
oauth = OAuth(app)
oauth.register(
    name="github",
    client_id = settings.CLIENT_ID,
    client_secret = settings.CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route("/")
def hello_world():
    return "<h1>Secret area!</h1>"

@app.route("/login")
def login():
    github = oauth.create_client('github')
    redirect_uri = 'https://python-oauth2-test.herokuapp.com/authorize'
    return github.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    resp.raise_for_status()
    profile = resp.json()
    print(token)
    print(profile)
    return redirect(url_for("hello_world"))
