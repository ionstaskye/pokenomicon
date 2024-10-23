import os
from unittest import TestCase

from models import db, connect_db, Team, User

os.environ['DATABASE_URL'] = "postgresql:///pokenomicon-test"

from app import app, CURR_USER_KEY

with app.app_context(): db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class TeamTestCase(TestCase):
    """Test teams."""

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()
            Team.query.delete()

            self.client = app.test_client()

            self.testuser = User.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        image_url=None)
            db.session.add(self.testuser)
            db.session.commit()

    def test_add_team(self):
        """Can user add a message?"""
        
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        with app.app_context():
            with self.client as c:
                testuser = User.query.first()
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = testuser.id

                    
                    resp = c.post("/teams/new", data ={'gen': 'generation-i', 'name': 'base'})

                    self.assertEqual(resp.status_code, 302)
                    team = Team(name= "base")
                    testuser.messages.append(message) 
                    msg = Message.query.first()
                    self.assertEqual(team.name, "base")