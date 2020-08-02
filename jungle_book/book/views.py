from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
from jungle_book.auth.jwt import token_required

from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.book.models import Book
from jungle_book.errors import error_book, error_user
from jungle_book.utils import update_query_object


book_bp = Blueprint('book_bp', __name__)


@book_bp.route("/book", methods=['POST'])
@token_required
def create_book(user):
    """Creates new book in db.

    request body args: user_id, avatar_image, name, description
    """

    name = request.json['name']
    description = request.json['description']
    avatar_image = request.json['avatar_image']


    try:
        if not user:
            return error_user.not_exists()
        else:
            new_book = Book(
                user_id=user.id,
                created_at=datetime.now(),
                last_update=datetime.now(),
                avatar_image=avatar_image,
                name=name,
                description=description
            )
            db.session.add(new_book)
            db.session.commit()

    except Exception as e:
        return error_book.unable_to_create(e)

    data = {
        'message': 'New Book created',
        'success': True
    }

    return make_response(jsonify(data), 200)


# TODO rethink query params structure
@book_bp.route("/book/<int:book_id>", methods=['DELETE'])
@token_required
def delete_book(user, book_id):
    """Deletes existing Book from database.

    url query params: book_id, user_id
    """

    try:
        result = Book.query.filter_by(user_id=user.user_id, id=book_id).first()
        if not result:
            return error_book.not_exists()
        else:
            db.session.delete(result)
            db.session.commit()

    except Exception as e:
        return error_book.unable_to_delete(e)

    data = {
        'message': 'Book deleted',
        'success': True
    }

    return make_response(jsonify(data), 200)


@book_bp.route("/book", methods=['PUT'])
@token_required
def update_book(user):
    """Updates existing book in database.

    request body args: book_id, user_id, name, description, avatar_image
    """

    json_data = request.get_json()
    user_id = user.id
    book_id = json_data['book_id']
    json_data['last_update'] = datetime.now()

    try:
        result = Book.query.filter_by(user_id=user_id, id=book_id).first()
        if not result:
            return error_book.not_exists()
        else:
            exceptions = ['user_id', 'book_id']
            updated_query = update_query_object(
                result, json_data, exceptions
            )

        db.session.add(updated_query)
        db.session.commit()

    except Exception as e:
        return error_book.unable_to_update(e)

    res_data = jsonify({
        'message': 'Book updated',
        'success': True
    })

    return make_response(res_data, 200)


@book_bp.route('/book/<book_id>', methods=['GET'])
def get_book(book_id):
    """
    Returns JSON with specific Book data

    :param (int): book_id
    """

    try:
        result = Book.query.filter_by(id=book_id).first()
        if not result:
            return error_book.not_exists()
        else:
            query_data = result.serialize

    except Exception as e:
        return error_book.not_exists(e)

    res_data = jsonify({
        'data': query_data,
        'success': True
    })

    return make_response(res_data, 200)
