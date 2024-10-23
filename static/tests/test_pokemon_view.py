import os
from unittest import TestCase

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///pokenomicon-test"

class PokemonViewTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()


            self.client = app.test_client()

            self.testuser = User.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        image_url=None)
            db.session.add(self.testuser)
            db.session.commit()

    def get_pokemon_page(self):
        """Checks to make sure a pokemon page loads"""

        with app.app_context():

            with app.app_context():
            with self.client as c:
                testuser = User.query.first()
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = testuser.id

                    resp = c.get("/pokemon/mankey")

                    self.assertEqual(resp.status_code, 200)