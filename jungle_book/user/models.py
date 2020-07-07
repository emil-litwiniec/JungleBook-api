from jungle_book.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    settings = db.Column(db.JSON)
    # TODO -> set path to default avatar picture
    avatar_image = db.Column(db.String())

    books = db.relationship('Book', backref="User", lazy=True)

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
            'books': self.books
        }

    def __repr__(self):
        return '<User %r>' % self.email
