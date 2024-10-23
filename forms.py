from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired



class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Edit User Form"""

    username = StringField("Username",validators = [InputRequired()])
    email = StringField("E-mail", validators = [InputRequired(), Email()])
    password = PasswordField("Password", validators = [InputRequired()])

class TeamForm(FlaskForm):
    """Adding a Team Form"""

    name = StringField("Name", validators = [InputRequired(),Length(max=20)])
    gen = SelectField("Generation", validators =[InputRequired()])

class PokemonForm(FlaskForm):
    """Form for selecting a pokemon"""

    pokemon = SelectField("Pokemon", validators = [InputRequired()])

class PokemonDetailForm(FlaskForm):
    """Form for putting details for chosen pokemon"""

    nature = SelectField("Nature", validators = [InputRequired()])
    ability = SelectField("Ability", validators = [InputRequired()])
    move_1 = SelectField("Move 1", validators = [InputRequired()])
    move_2 = SelectField("Move 2", validators = [InputRequired()])
    move_3 = SelectField("Move 3", validators = [InputRequired()])
    move_4 = SelectField("Move 4", validators = [InputRequired()])