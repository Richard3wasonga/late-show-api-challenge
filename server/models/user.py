from . import db, SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, SerializerMixin):
    __tablename__= "users"

    serialize_rules = ('-appearances.user', '-password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>" 
