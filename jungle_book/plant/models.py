from jungle_book.db import db


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    encyclopedia_id = db.Column(db.Integer, db.ForeignKey('encyclopedia.id'))
    last_watering = db.Column(db.DateTime(timezone=False))
    waterings = db.Column(db.JSON)
    last_dew = db.Column(db.DateTime(timezone=False))
    dews = db.Column(db.JSON)
    stats = db.Column(db.JSON)

    moments = db.relationship('Moment', backref="plant", lazy=True)

    @property
    def serialze(self):
        return {
            'id': self.id,
            'name': self.name,
            'book_id': self.book_id,
            'encyclopedia_id': self.encyclopedia_id,
            'last_watering': self.last_watering,
            'waterings': self.waterings,
            'last_dew': self.last_dew,
            'dews': self.dews,
            'stats': self.stats,
            'moments': self.moments
        }
    
    def __repr__(self):
        return '<Plant %r>' % self.id
