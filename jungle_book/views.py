from flask import (Blueprint, url_for, render_template,
                   redirect, request, jsonify, Response, abort)
import operator
from authlib.flask.client import OAuth
# from authlib.jose import jwt as jose_jwt
from google.auth import jwt as google_jwt
from datetime import datetime
from .models import db, User
from .jwt import encode_jwt, decode_jwt, extend_jwt


# from jungle_book import oauth
route_blueprint = Blueprint('route_blueprint', __name__)

oauth = OAuth()
oauth.register(
    name="google",
    client_id="810979674149-i58pjaopuunstb60n6j645nhb9mvk66e.apps.googleusercontent.com",
    client_secret="DVVkppPgpEFDX5S7naVvLGjA",
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com',
    client_kwargs={'scope': 'email profile openid'},
    redirect_uri="http://localhost:5000/"
 )


@route_blueprint.route("/", methods=["GET"])
def index():
    return "Hello"


@route_blueprint.route('/login', methods=["GET"])
def login():
    redirect_uri = url_for('route_blueprint.authorize_signup', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@route_blueprint.route('/token/extend', methods=["PUT"])
def extend_token():
    token = request.json['token']
    return extend_jwt(token=token)


@route_blueprint.route('/authorize-signup', methods=["GET", "POST"])
def authorize_signup():

    token_first_name = request.json['given_name']
    token_last_name = request.json['family_name']
    token_email = request.json['email']

    # --- these will run in prodcution --- #

    # token = oauth.google.authorize_access_token()
    # data_token = google_jwt.decode(token['id_token'], verify=False)
    # token_email = data_token['email']

    # ------------------------------------ #

    try:
        results = User.query.filter_by(email=token_email).first()
        if not results:
            new_user = User(
                first_name=token_first_name,
                last_name=token_last_name,
                email=token_email,
                created_at=datetime.now(),
                last_update=datetime.now()
            )

            db.session.add(new_user)
            db.session.commit()
        else:
            print(f'Welcome back {results.first_name}!')
    except:
        return abort(400, Response("Unable to connect to database."))

    id_results = User.query.filter_by(email=token_email).first()
    payload = {
        "id": id_results.id,
        "first_name": id_results.first_name,
        "last_name": id_results.last_name,
        "email": id_results.email
    }
    new_token = encode_jwt(payload=payload)

    return jsonify({
        "access_token": new_token
    })
