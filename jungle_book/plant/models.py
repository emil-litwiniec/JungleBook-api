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
    
    def __repr__(self):
        return '<Plant %r>' % self.id
