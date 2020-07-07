from jungle_book.db import db


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    encyclopedia_id = db.Column(db.Integer, db.ForeignKey('encyclopedia.id'))
    plant_info = db.Column(db.JSON)
    last_watering = db.Column(db.DateTime(timezone=False))
    waterings = db.Column(db.JSON)
    last_dew = db.Column(db.DateTime(timezone=False))
    dews = db.Column(db.JSON)
    stats = db.Column(db.JSON)
    created_at = db.Column(db.DateTime(timezone=False))
    last_update = db.Column(db.DateTime(timezone=False))
    avatar_image = db.Column(db.String())

    moments = db.relationship('Moment', backref="plant", lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'book_id': self.book_id,
            'encyclopedia_id': self.encyclopedia_id,
            'plant_info': self.plant_info,
            'last_watering': self.last_watering,
            'waterings': self.waterings,
            'last_dew': self.last_dew,
            'dews': self.dews,
            'stats': self.stats,
            'created_at': self.created_at,
            'last_update': self.last_update,
            'avatar_image': self.avatar_image,
            'moments': self.moments
        }

    def __repr__(self):
        return '<Plant %r>' % self.id
