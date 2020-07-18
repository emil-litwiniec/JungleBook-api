from flask import Blueprint, request, make_response, jsonify, abort
from datetime import datetime
import json

from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.plant.models import Plant
from jungle_book.book.models import Book

from jungle_book.errors import error_plant, error_book, error_user

from jungle_book.utils import update_query_object

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/sign-up', methods=['POST'])
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
            return abort(400, 'Email already in use')
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

    data = {
        'message': 'New User created',
        'success': True
    }

    return make_response(jsonify(data), 200)

