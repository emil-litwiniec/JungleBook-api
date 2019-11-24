from flask import (Blueprint, url_for,
                   redirect, request, jsonify, Response, abort)
# from google.auth import jwt as google_jwt  # required for production
from datetime import datetime
from jungle_book.user.models import User
from jungle_book.db import db
from .jwt import encode_jwt, extend_jwt
from .oauth import oauth


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/", methods=["GET"])
def index():
    return "Hello"


@auth_bp.route('/login', methods=["GET"])
def login():
    redirect_uri = url_for('auth_bp.authorize_signup', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/token/extend', methods=["PUT"])
def extend_token():
    token = request.json['token']
    return extend_jwt(token=token)


@auth_bp.route('/authorize-signup', methods=["GET", "POST"])
def authorize_signup():
    token_first_name = request.json['given_name']
    token_last_name = request.json['family_name']
    token_email = request.json['email']

    # --- these will run in prodcution --- #

    # token = oauth.google.authorize_access_token()
    # data_token = google_jwt.decode(token['id_token'], verify=False)
    # token_email = data_token['email']
    # token_first_name = data_token['given_name']
    # token_last_name = data_token['family_name']

    # ------------------------------------ #

    # print(request.json['email'])

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
    except Exception as e:
        print(e)
        return abort(500, "Something wrong with the query")
        # return "Something wrong with the query"

    id_results = User.query.filter_by(email=token_email).first()

    # print(id_results.id)
    payload = {
        "id": id_results.id,
        "first_name": id_results.first_name,
        "last_name": id_results.last_name,
        "email": id_results.email
    }

    new_token = encode_jwt(payload=payload)
    response = jsonify({'access-token': str(new_token)})

    return response

# @auth_bp.route("/validate-token", methods=["POST"])
# def validate_token():
#     pass
