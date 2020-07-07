from flask import Blueprint, request, make_response, jsonify, flash
import os
import uuid
from datetime import datetime
from jungle_book.errors import ErrorHandler, error_plant, error_book, error_user
from jungle_book.db import db
from jungle_book.user.models import User
from jungle_book.book.models import Book
from jungle_book.plant.models import Plant
from jungle_book.utils import update_query_object
from werkzeug.utils import secure_filename
from enum import Enum
from jungle_book.fs.fs_manager import FileSystemManager
from flask_cors import

remove_file = FileSystemManager.remove
files_bp = Blueprint('files_bp', __name__)

CURRENT_DIRECTORY = os.getcwd()
UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class ROLE(Enum):
    PLANT = 1
    ROLE = 2
    USER = 3


@files_bp.after_request  # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = "Content-Type, Authorization"
    header['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@files_bp.route("/files/<int:user_id>", methods=['POST'])
def file_upload(user_id):
    files = request.files
    if 'image' not in files:
        return ErrorHandler.abort(400, "No file selected")

    file = files['image']
    if file.filename == '':
        return ErrorHandler.abort(400, "No file selected")

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            ext = filename.split('.')[-1]
            new_filename = f"{uuid.uuid4()}.{ext}"
            path_to_file = os.path.join(UPLOAD_FOLDER, str(user_id),
                                        new_filename)
            file.save(os.path.join(CURRENT_DIRECTORY, path_to_file))
        except FileNotFoundError as e:
            print(e)
            return ErrorHandler.abort(400, "No such file or directory")

    res_data = jsonify({
        'message': 'File uploaded',
        'filename': new_filename,
        'success': True
    })

    return make_response(res_data, 200)


@files_bp.route("/files", methods=['DELETE'])
def file_remove():
    json_data = request.get_json()
    try:
        role_id = json_data['role_id']
        user_id = json_data['user_id']
        filename = json_data['filename']
        role = json_data['role']
    except Exception:
        return ErrorHandler.provide_parameters()

    path_to_file = os.path.join(UPLOAD_FOLDER, str(user_id),
                                filename)
    data = {
        'last_update': datetime.now(),
        'avatar_image': ''
    }

    if role == ROLE.PLANT.value:
        try:
            plant = Plant.query.filter_by(id=role_id).first()
            print('plant: ', plant)
            updated_plant = update_query_object(
                plant, data
            )
            db.session.add(updated_plant)
            db.session.commit()
        except Exception:
            return error_plant.unable_to_update()
        # remove_file(path_to_file)
    elif role == ROLE.BOOK.value:
        try:
            book = Book.query.filter_by(id=role_id).first()
            updated_book = update_query_object(
                book, data
            )
            db.session.add(updated_book)
            db.session.commit()
        except Exception:
            return error_book.unable_to_update()
        # remove_file(path_to_file)
    elif role == ROLE.USER.value:
        try:
            user = User.query.filter_by(id=role_id).first()
            updated_user = update_query_object(
                user, data
            )
            db.session.add(updated_user)
            db.session.commit()
        except Exception:
            return error_user.unable_to_update()
        # remove_file(path_to_file)
    else:
        return ErrorHandler.abort(400, 'No such role')

    data = {
        'message': 'File removed',
        'filename': filename,
        'success': True
    }

    return jsonify(data)
