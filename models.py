"""Pokemon Models"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

class Pokemon(db.Model):
    """Pokemon model"""

    __tablename__ = "pokemon"

    id = db.Column(db.Integer,
                    primary_key = True
                    )
    name = db.Column(db.Text,
                    nullable = False)
    abilities = db.Column(db.Text,
                        nullable = False)
    nature = db.Column(db.Text,
                        nullable = False)
    move_one = db.Column(db.Text,
                        nullable = False)
    move_two = db.Column(db.Text)
    move_three = db.Column(db.Text)
    move_four = db.Column(db.Text)
    team_id = db.Column(db.Integer,
                    db.ForeignKey("teams.id", ondelete = 'CASCADE'))

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    teams = db.relationship("Teams")


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,

        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Teams(db.Model):
    """Model for Teams"""

    __tablename__ = 'teams'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    gen = db.Column(db.Text,
        nullable = False)

    name = db.Column(db.Text, 
                    nullable = False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    
    pokemon = db.relationship("Pokemon")

    
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)



    
