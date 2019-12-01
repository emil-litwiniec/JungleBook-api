from flask import Blueprint, request, abort, make_response, jsonify
from datetime import datetime

from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.book.models import Book


def updateQueryObject(query, data, exceptions):
    for (k, v) in data.items():
        if k in exceptions:
            continue
        query.__setattr__(k, v)
    return query


no_such = 'No such user or book'


book_bp = Blueprint('book_bp', __name__)


@book_bp.route("/book", methods=['POST'])
def create_book():
    """
    Creates new book in database.
    request body args: user_id, avatar_image, name, description
    """

    user_id = request.json['user_id']
    name = request.json['name']
    description = request.json['description']
    avatar_image = request.json['avatar_image']

    try:
        results = User.query.filter_by(id=user_id).first()
        if not results:
            return abort(400, "User doesn't exist")
        else:
            new_book = Book(
                user_id=user_id,
                created_at=datetime.now(),
                last_update=datetime.now(),
                avatar_image=avatar_image,
                name=name,
                description=description
            )
            db.session.add(new_book)
            db.session.commit()

    except Exception as e:
        print(e)
        return abort(500, "Unable to create new book")

    data = {
        'message': 'New Book created',
        'success': True
    }

    return make_response(jsonify(data), 200)


@book_bp.route("/book/<int:user_id>,<int:book_id>", methods=['DELETE'])
def delete_book(user_id, book_id):
    """
    Deletes existing book in database.
    url query params: book_id, user_id
    """

    try:
        result = Book.query.filter_by(user_id=user_id, id=book_id).first()
        if not result:
            return abort(400, no_such)
        else:
            db.session.delete(result)
            db.session.commit()

    except Exception as e:
        print(e)
        return abort(500, "Unable to delete a book")

    data = {
        'message': 'Book deleted',
        'success': True
    }

    return make_response(jsonify(data), 200)


@book_bp.route("/book", methods=['PUT'])
def update_book():
    """
    Updates existing book in database.
    request body args: book_id, user_id, name, description, avatar_image
    """

    json_data = request.get_json()
    user_id = json_data['user_id']
    book_id = json_data['book_id']
    json_data['last_update'] = datetime.now()

    try:
        result = Book.query.filter_by(user_id=user_id, id=book_id).first()
        if not result:
            return abort(400, no_such)
        else:
            exceptions = ['user_id', 'book_id']
            updated_query = updateQueryObject(
                result, json_data, exceptions
            )

        db.session.add(updated_query)
        db.session.commit()

    except Exception as e:
        print(e)
        return abort(500, "Unable to update a book")

    data = {
        'message': 'Book updated',
        'success': True
    }

    return make_response(jsonify(data), 200)
