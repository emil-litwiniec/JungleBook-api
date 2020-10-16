from jungle_book.db import db
from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    settings = db.Column(db.JSON)
    avatar_image = db.Column(db.String())
    _password = db.Column(db.String(128))

    books = db.relationship('Book', backref="User", lazy=True)
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, text_password):
        self._password = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def validate_password(self, text_password):
        if not self._password:
            return False
        return bcrypt.check_password_hash(self._password, text_password)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
            'last_update': self.last_update,
            'settings': self.settings,
            'avatar_image': self.avatar_image,
            'books': [book.serialize for book in self.books],
        }

    def __repr__(self):
        return '<User %r>' % self.email
