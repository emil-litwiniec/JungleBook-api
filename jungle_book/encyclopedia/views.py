from flask import Flask, Blueprint, request, abort, make_response, jsonify
import os
from datetime import datetime
import requests

from jungle_book.db import db
# from jungle_book.user.models import User
# from jungle_book.book.models import Plant
from jungle_book.encyclopedia.models import Encyclopedia
from jungle_book.errors import ErrorHandler
from jungle_book.utils import update_query_object

encyclopedia_bp = Blueprint('encyclopedia_bp', __name__)

@encyclopedia_bp.route('/encyclopedia', methods=['POST'])
def create_species():
    json_data = request.get_json()
    common_name = json_data['common_name']

    try:
        result = Encyclopedia.query.filter_by(common_name=common_name, validated=True)

        if not result:
            new_species = update_query_object(
                Encyclopedia(), json_data
            )

            db.session.add(new_species)
            db.session.commit()


    except Exception as e:
        return abort(404)

