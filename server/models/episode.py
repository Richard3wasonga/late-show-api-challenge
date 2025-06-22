from . import db, SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

class Episode(db.Model, SerializerMixin):
    __tablename__= "episodes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship("Appearance", back_populates="episode", cascade="all, delete-orphan")
    guests = association_proxy("appearances", "guest" creator=lambda guest: Appearance(guest=guest))

    def __repr__(self):
        return f"<Episode id={self.id} number={self.number} date={self.date}>"