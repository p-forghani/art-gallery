from app import db
from datetime import datetime

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    tag_id = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'tag_id': self.tag_id,
            'price': self.price,
            'date_created': self.date_created.isoformat()
        }
