from jungle_book.db import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    guest_user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    avatar_image = db.Column(db.String())

    plants = db.relationship('Plant', backref="book", lazy=True)

    def __repr__(self):
        return '<Book %r>' % self.id
