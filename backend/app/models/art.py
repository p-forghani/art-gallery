from datetime import datetime
from bson import ObjectId

class Art:
    def __init__(self, name, description, category_id=None, tag_id=None, price=None, image_path=None, created_at=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.category_id = category_id
        self.tag_id = tag_id
        self.price = price
        self.image_path = image_path
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "tag_id": self.tag_id,
            "price": self.price,
            "image_path": self.image_path,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data['description'],
            category_id=data.get('category_id'),
            tag_id=data.get('tag_id'),
            price=data.get('price'),
            image_path=data.get('image_path'),
            created_at=data.get('created_at'),
            _id=ObjectId(data['_id']) if '_id' in data else None
        )
