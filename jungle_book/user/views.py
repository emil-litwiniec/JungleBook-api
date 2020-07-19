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
