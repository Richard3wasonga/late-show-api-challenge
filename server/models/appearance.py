from . import db, SerializerMixin
from sqlalchemy.orm import validates

class Appearance(db.Model, SerializerMixin):
    __tablename__= "appearances"

    serialize_rules = ('-guest.appearances', '-episode.appearances')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest = db.relationship("Guest", back_populates="appearances")
    episode = db.relationship("Episode", back_populates="appearances")

    @validates("rating")
    def validate_rating(self, key, value):
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    def __repr__(self):
        return (
            f"<Appearance id={self.id} guest_id={self.guest_id} "
            f"episode_id={self.episode_id} rating={self.rating}>"
        )