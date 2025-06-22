import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from random import randint, sample, choice as rc
from datetime import date, timedelta
from faker import Faker
from app import app
from models import db, Guest, Episode, Appearance, User

fake = Faker()

with app.app_context():
    print("Seeding realistic data...")

    try:

        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        User.query.delete()
        db.session.commit()

    
        occupations = [
            "Actor", "Comedian", "Politician", "Musician", "Author",
            "Scientist", "Entrepreneur", "Athlete", "Chef", "YouTuber"
        ]

        guests = [Guest(name=fake.name(), occupation=rc(occupations)) for _ in range(10)]
        db.session.add_all(guests)
        db.session.commit()

        
        episodes = [
            Episode(
                date=date.today() - timedelta(weeks=i),
                number=i + 1
            ) for i in range(10)
        ]
        db.session.add_all(episodes)
        db.session.commit()

        
        appearances = []
        for episode in episodes:
            selected_guests = sample(guests, randint(1, 3))
            for guest in selected_guests:
                appearances.append(Appearance(
                    guest_id=guest.id,
                    episode_id=episode.id,
                    rating=randint(2, 5)
                ))
        db.session.add_all(appearances)

        
        test_user = User(username="latetest")
        test_user.set_password("securepass123")
        db.session.add(test_user)

        db.session.commit()
        print(f"Seeded {len(guests)} guests, {len(episodes)} episodes, {len(appearances)} appearances.")
        print("Done seeding realistic data.")

    except Exception as e:
        db.session.rollback()
        print("An error occurred during seeding:", e)