from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import json

from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.plant.models import Plant
from jungle_book.book.models import Book

from jungle_book.errors import error_plant, error_book

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


@plant_bp.route("/plant/watering", methods=['PUT'])
def update_watering():
    """Updates existing Plant's watering in database.

    # request body args: plant_id
    """

    json_data = request.get_json()
    plant_id = json_data['plant_id']
    json_data['last_update'] = datetime.now()
    json_data['last_watering'] = datetime.now().isoformat()


    try:
        result = Plant.query.filter_by(id=plant_id).first()
        if not result:
            return error_plant.not_exists()
        else:
            current_time = json_data['last_watering']
            if result.waterings is None:
                json_data['waterings'] = json.dumps({
                    'waterings': [
                        current_time
                    ]
                })
            else:
                waterings = json.loads(result.waterings)
                waterings['waterings'].append(current_time)
                json_data['waterings'] = json.dumps(waterings)

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


@plant_bp.route("/plant/dew", methods=['PUT'])
def update_dew():
    # TODO: encapsulate dew and watering update views, as they use the same
    #       logic
    """Updates existing Plant's dew in database.

    # request body args: plant_id
    """

    json_data = request.get_json()
    plant_id = json_data['plant_id']
    json_data['last_update'] = datetime.now().isoformat()
    json_data['last_dew'] = datetime.now()

    try:
        result = Plant.query.filter_by(id=plant_id).first()
        if not result:
            return error_plant.not_exists()
        else:
            current_time = datetime.timestamp(json_data['last_dew'])
            if result.dews is None:
                json_data['dews'] = json.dumps({
                    'dews': [
                        current_time
                    ]
                })
            else:
                dews = json.loads(result.dews)
                dews['dews'].append(current_time)
                json_data['dews'] = json.dumps(dews)

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
