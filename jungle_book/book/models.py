from jungle_book.db import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(35))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    guest_user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    avatar_image = db.Column(db.String(), nullable=True)

    plants = db.relationship('Plant', backref="book", lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'guest_user_id': self.guest_user_id,
            'created_at': self.created_at,
            'last_update': self.last_update,
            'avatar_image': self.avatar_image,
            'plants': [plant.serialize for plant in self.plants]
        }

    def __repr__(self):
        return '<Book %r>' % self.id
