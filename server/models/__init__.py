from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
SerializerMixin = SerializerMixin

from .user import User
from .guest import Guest
from .episode import Episode
from .appearance import Appearance
from .token_blocklist import TokenBlocklist