from jungle_book.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    settings = db.Column(db.JSON)
    avatar_image = db.Column(db.String())  # TODO -> set path to default avatar picture

    books = db.relationship('Book', backref="User", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email
