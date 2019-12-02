from jungle_book.db import db


class Encyclopedia(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    common_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    info = db.Column(db.JSON)

    plants = db.relationship('Plant', backref="encyclopedia", lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'common_name': self.common_name,
            'description': self.description,
            'info': self.info
        }

    def __repr__(self):
        return '<Encyclopedia %r>' % self.id
