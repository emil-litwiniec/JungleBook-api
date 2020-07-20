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


@user_bp.route('/user/<int:user_id>', methods=["GET"])
def get_user_data(user_id):
    res_data = ''
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            error_user.not_exists()
        else:
            query_data = user.serialize
    except Exception as e:
        return error_user.not_exists(e)
    
    res_data = jsonify({
        'data': query_data,
        'success': True
    })

    return make_response(res_data, 200)