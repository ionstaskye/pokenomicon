from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Pokemon, Teams


os.environ['DATABASE_URL'] = "postgresql:///pokenomicon-test"

with app.app_context(): db.create_all()

class TeamModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():    
            db.drop_all()
            db.create_all()

            self.uid = 94566
            u = User.signup("testing", "testing@test.com", "password", None)
            u.id = self.uid
            db.session.commit()

            self.u = User.query.get(self.uid)

            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res

    def test_team_model(self):
        """Does team model work?"""

        with app.app_context():
            user= User.query.first()
            t = Team(
                gen="generation-i",
                name= "base",
                user_id=user.id
            )

            db.session.add(t)
            db.session.commit()

    
            self.assertEqual(len(user.teams), 1)
            self.assertEqual(user.teams[0].name, "base")

    def test_pokemon_model(self):
        """Does pokemon model work?"""

        with app.app_context():
            user= User.query.first()
            t = Team(
                gen="generation-i",
                name= "base",
                user_id=user.id
            )

            db.session.add(t)
            db.session.commit()

            p = Pokemon(
                name = "mankey",
                abilitiy = "vital spirit",
                nature = 'hardy',
                move_one = 'scratch',
                move_two = 'thrash',
                move_three = 'seisimic toss',
                move_four = 'bide'
                team_id = t.id
            )

            db.session.add(p)
            db.session.commit()

            self.assertEqual(len(t.pokemon), 1)
            self.assertEqual(t.pokemon[0].name, "mankey")
