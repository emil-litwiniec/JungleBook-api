from jungle_book.db import db


class Moment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    last_update = db.Column(db.DateTime(timezone=False))
    description = db.Column(db.Text)
    snapshots = db.Column(db.JSON)

    def __repr__(self):
        return '<Moment %r>' % self.id
