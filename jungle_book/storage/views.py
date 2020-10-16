import uuid
import os
from flask import Blueprint, request, make_response, jsonify
from jungle_book.errors import ErrorHandler, error_plant, error_book, error_user
from werkzeug.utils import secure_filename

from .storage import file_upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


storage_bp = Blueprint('storage_bp', __name__)


@storage_bp.route('/upload', methods=["POST"])
def upload_image():
    files = request.files
    if 'image' not in files:
        return ErrorHandler.abort(400, "No file selected")

    file = files['image']
    if file.filename == '':
        return ErrorHandler.abort(400, "No file selected")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        try:
            file_upload(new_filename, file)
        except Exception:
            return ErrorHandler.abort(400)

        res_data = jsonify({
            'data': {
                'filename': new_filename
            },
            'success': True
        })

        return make_response(res_data, 200)
