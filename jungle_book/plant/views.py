from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import json

from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.plant.models import Plant
from jungle_book.book.models import Book

from jungle_book.errors import error_plant, error_book, ErrorHandler

from jungle_book.utils import update_query_object

plant_bp = Blueprint('plant_bp', __name__)


@plant_bp.route('/plant', methods=['POST'])
def create_plant():
    """Creates new Plant in db
    """

    json_data = request.get_json()
    book_id = json_data['book_id']
    json_data['last_update'] = datetime.now()
    json_data['created_at'] = datetime.now()

    try:
        result = Book.query.filter_by(id=book_id).first()
        if not result:
            return error_book.not_exists()
        else:
            new_plant = update_query_object(
                Plant(), json_data
            )
            db.session.add(new_plant)
            db.session.commit()

    except Exception as e:
        return error_plant.unable_to_create(e)

    data = {
        'plant_id': new_plant.id,
        'message': 'New Plant created',
        'success': True
    }

    return make_response(jsonify(data), 200)


@plant_bp.route("/plant/<int:plant_id>", methods=['DELETE'])
def delete_plant(plant_id):
    """Deletes existing Plant from database.

    url query params: plant_id
    """

    try:
        result = Plant.query.filter_by(id=plant_id).first()
        if not result:
            return error_plant.not_exists()
        else:
            db.session.delete(result)
            db.session.commit()

    except Exception as e:
        return error_plant.unable_to_delete(e)

    data = {
        'message': 'Plant deleted',
        'success': True
    }

    return make_response(jsonify(data), 200)


@plant_bp.route("/plant", methods=['PUT'])
def update_plant():
    """Updates existing Plant in database.

    # request body args: plant_id, name, description, avatar_image
    """

    json_data = request.get_json()
    plant_id = json_data['plant_id']
    json_data['last_update'] = datetime.now()

    try:
        result = Plant.query.filter_by(id=plant_id).first()
        if not result:
            return error_plant.not_exists()
        else:
            exceptions = ['id', 'book_id']
            updated_query = update_query_object(
                result, json_data, exceptions
            )

        db.session.add(updated_query)
        db.session.commit()

    except Exception as e:
        return error_plant.unable_to_update(e)

    res_data = jsonify({
        'message': 'Plant updated',
        'success': True
    })

    return make_response(res_data, 200)


@plant_bp.route("/plant/<action>", methods=['PUT'])
def plant_update_action(action):
    if action not in ['dew', 'watering']:
        return ErrorHandler.abort()

    json_data = request.get_json()
    plant_ids = json_data['plant_ids']
    json_data['last_update'] = datetime.now()
    json_data['last_{}'.format(action)] = datetime.now().isoformat()

    if not plant_ids:
        return error_plant.provide_parameters()

    try:
        results = Plant.query.filter(Plant.id.in_(plant_ids)).all()
        if not results:
            return error_plant.not_exists()
        else:
            for result in results:
                current_time = json_data['last_{}'.format(action)]
                last_action = getattr(result, '{}s'.format(action))

                if last_action is None:
                    json_data['{}s'.format(action)] = json.dumps({
                        ['{}s'.format(action)]: [
                            current_time
                        ]
                    })
                else:
                    action_property = json.loads(last_action)
                    action_property['{}s'.format(action)].append(current_time)
                    json_data['{}s'.format(action)] = json.dumps(
                        action_property)

                exceptions = ['id', 'book_id']
                updated_query = update_query_object(
                    result, json_data, exceptions
                )

                db.session.add(updated_query)
                db.session.commit()

    except Exception as e:
        return error_plant.unable_to_update(e)

    res_data = jsonify({
        'message': 'Plant updated',
        'success': True
    })

    return make_response(res_data, 200)


@plant_bp.route("/plant/update_book", methods=['PUT'])
def update_plants_book():
    """Updates existing Plant's book_id in database.

    # request body args: book_id, plant_id
    """

    json_data = request.get_json()
    plant_id = json_data['plant_id']
    book_id = json_data['book_id']
    json_data['last_update'] = datetime.now()

    try:
        new_book = Book.query.filter_by(id=book_id).first()
        plant = Plant.query.filter_by(id=plant_id).first()

        if not new_book:
            return error_book.not_exists()
        if not plant:
            return error_plant.not_exists()
        else:
            exceptions = ['id']
            updated_query = update_query_object(
                plant, json_data, exceptions
            )

            db.session.add(updated_query)
            db.session.commit()

    except Exception as e:
        return error_plant.unable_to_update(e)

    res_data = jsonify({
        'message': "Plant's Book updated",
        'success': True
    })

    return make_response(res_data, 200)


@plant_bp.route('/plant/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    """
    Returns JSON with specific Plant data

    :param (int): plant_id
    """

    try:
        result = Plant.query.filter_by(id=plant_id).first()
        if not result:
            return error_plant.not_exists()
        else:
            query_data = result.serialize

    except Exception as e:
        return error_plant.not_exists(e)

    res_data = jsonify({
        'data': query_data,
        'success': True
    })

    return make_response(res_data, 200)
