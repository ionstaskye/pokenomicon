
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Teams


os.environ['DATABASE_URL'] = "postgresql:///pokenomicon-test"



with app.app_context(): db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            u1 = User.signup("test1", "email1@email.com", "password", None)
            uid1 = 1111
            u1.id = uid1

            db.session.commit()

            u1 = User.query.get(uid1)


            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res

    def test_user_model(self):
        """Does basic model work?"""

        with app.app_context():
            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            # User should have no messages & no followers
            self.assertEqual(len(u.teams), 0)

    def test_valid_signup(self):
        with app.app_context():
            u_test = User.signup(
                "testtesttest", "testtest@test.com", "password", None)
            uid = 99999
            u_test.id = uid
            db.session.commit()

            u_test = User.query.get(uid)
            self.assertIsNotNone(u_test)
            self.assertEqual(u_test.username, "testtesttest")
            self.assertEqual(u_test.email, "testtest@test.com")
            self.assertNotEqual(u_test.password, "password")

    def test_invalid_username_signup(self):
        with app.app_context():
            invalid = User.signup(None, "test@test.com", "password", None)
            uid = 123456789
            invalid.id = uid
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

     def test_invalid_email_signup(self):
        with app.app_context(): 
            invalid = User.signup("testtest", None, "password", None)
            uid = 123789
            invalid.id = uid
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    def test_invalid_password_signup(self):
        with app.app_context():
            with self.assertRaises(ValueError) as context:
                User.signup("testtest", "email@email.com", "", None)

            with self.assertRaises(ValueError) as context:
                User.signup("testtest", "email@email.com", None, None)