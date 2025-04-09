from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    def __init__(self, email, name, password_hash=None, is_admin=False, _id=None):
        self._id = _id or ObjectId()
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            '_id': str(self._id),
            'email': self.email,
            'name': self.name,
            'is_admin': self.is_admin
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data['email'],
            name=data['name'],
            password_hash=data.get('password_hash'),
            is_admin=data.get('is_admin', False),
            _id=ObjectId(data['_id']) if '_id' in data else None
        )
