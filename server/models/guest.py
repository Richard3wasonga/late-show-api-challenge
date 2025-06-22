from . import db, SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

class Guest(db.Model, SerializerMixin):
    __tablename__= "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String)
    appearance = db.relationship("Appearance", back_populates="guest", cascade="all, delete-orphan")
    episodes = association_proxy("appearances", "episode", creator=lambda epi: Appearance(episode=epi))

    def __repr__(self):
        return f"<Guest id={self.id} name='{self.name}' occupation='{self.occupation}'>"