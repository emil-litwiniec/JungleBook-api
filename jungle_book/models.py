from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, JSON, Integer
db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=False))
    last_update = Column(DateTime(timezone=False))
    settings = Column(JSON)
    avatar_image = Column(String())  # TODO -> set path to default avatar picture
