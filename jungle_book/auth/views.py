import os
from datetime import datetime

from flask import Blueprint, jsonify, make_response, redirect, request, url_for
from google.auth import jwt as google_jwt  # required for production
from jungle_book.db import db
from jungle_book.errors import ErrorHandler, error_user
from jungle_book.user.models import User

from .jwt import encode_jwt, extend_jwt
from .oauth import oauth

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/sign-in-with-google', methods=["GET"])
def login():
    redirect_uri = url_for('auth_bp.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/authorize', methods=["GET", "POST"])
def authorize_google():
    # try:
    #     token_first_name = request.json['given_name']
    #     token_last_name = request.json['family_name']
    #     token_email = request.json['email']
    # except Exception:
    #     return ErrorHandler.provide_parameters()
    # --- these will run in prodcution --- #

    token = oauth.google.authorize_access_token()
    data_token = google_jwt.decode(token['id_token'], verify=False)
    token_email = data_token['email']
    token_first_name = data_token['given_name']
    token_last_name = data_token['family_name']

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
    except Exception as e:
        return ErrorHandler.abort(500, "An error occured during authorization", e)

    id_results = User.query.filter_by(email=token_email).first()

    payload = {
        "id": id_results.id,
        "first_name": id_results.first_name,
        "last_name": id_results.last_name,
        "email": id_results.email
    }

    new_token = encode_jwt(payload=payload)
    response = jsonify({'access-token': str(new_token)})
    return redirect(os.environ['REDIRECT_URI']


@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    json_data = request.get_json()
    try:
        email = json_data['email']
        password = json_data['password']
    except Exception as e:
        return error_user.provide_parameters()

    try:
        result = User.query.filter_by(email=email).first()
        if result:
            return ErrorHandler.abort(400, 'Email already in use')
        else:
            new_user = User(
                first_name='',
                last_name='',
                email=email,
                password=password,
                created_at=datetime.now(),
                last_update=datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()

    except Exception as e:
        return error_user.unable_to_create(e)

    payload = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email
    }

    new_token = encode_jwt(payload=payload)
    response = jsonify({'access-token': str(new_token)})

    return make_response(response, 200)


@auth_bp.route('/sign-in', methods=['POST'])
def sign_in():
    json_data = request.get_json()
    try: 
        email = json_data['email']
        password = json_data['password']
    except Exception as e:
        return error_user.provide_parameters()

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return ErrorHandler.abort(400, 'No such user')
        else:
            if user.validate_password(password):
                print('validate_password 1')
                payload = {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email
                    }
                
                new_token = encode_jwt(payload=payload)
                response = jsonify({'access-token': str(new_token)})

                return make_response(response, 200)
            else:
                return ErrorHandler.abort(400, "Email or password are incorrect")

                
    except Exception as e:
        return error_user.unable_to_create(e)


@auth_bp.route('/token/extend', methods=["PUT"])
def extend_token():
    token = request.json['token']
    return extend_jwt(token=token)
