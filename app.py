import os, requests

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from models import db, connect_db, Pokemon, User, Teams
from forms import UserAddForm, EditUserForm, LoginForm, TeamForm, PokemonForm,PokemonDetailForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port = port)

DATABASE_URL = os.environ.get("DATABASE_URL")
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context(): db.create_all()

base_api = "https://pokeapi.co/api/v2/"
##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,

            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("Successfully logged out.")

    return redirect("/login")

@app.route("/")
def display_home_page():
    """Pulls up home page"""

    return render_template("home.html")

app.run()

@app.route("/pokemon")
def display_pokemon_page():
    """Pulls up Pokemon page"""
    
    resp = requests.get(f"{base_api}/type")
    types = resp.json()["results"]
    

    return render_template("pokemon.html", types = types)

@app.route("/pokemon/search")
def search_pokemon():
    """Search for specific pokemon"""

    data = request.args.get("name")

    resp = requests.get(f"{base_api}/pokemon/{data}")

    pokemon = resp.json()
    moves = pokemon['moves']
    abilities = pokemon['abilities']
    stats = pokemon['stats']
    sprites = pokemon['sprites']
    items = pokemon['held_items']
    types = len(pokemon['types'])
    versions = pokemon['game_indices']

    if resp.status_code == 200:

       return render_template("pokemon_info.html", versions = versions, items = items, pokemon = pokemon, moves = moves, abilities = abilities, stats = stats, sprites = sprites, types = types)

    else:
        return redirect ("/pokemon", error = "Pokemon not found")

@app.route("/pokemon/type/<type>")
def display_type_page(type):
    """Get and display data for type page"""

    resp = requests.get(f"{base_api}/type/{type}", params = {"limit": 100})

    pokemon = resp.json()['pokemon']

    return render_template("pokemon_type.html", pokemon = pokemon, type = type)

@app.route("/pokemon/<pokemon>")
def display_pokemon_info(pokemon):
    """Get and display info on pokemon"""

    resp = requests.get(f"{base_api}/pokemon/{pokemon}")

    pokemon = resp.json()
    moves = pokemon['moves']
    abilities = pokemon['abilities']
    stats = pokemon['stats']
    sprites = pokemon['sprites']
    items = pokemon['held_items']
    types = len(pokemon['types'])
    versions = pokemon['game_indices']

    return render_template("pokemon_info.html", versions = versions, items = items, pokemon = pokemon, moves = moves, abilities = abilities, stats = stats, sprites = sprites, types = types)

@app.route("/pokemon/<pokemon>/moves/<version>")
def display_pokemon_moves(pokemon, version):
    """get and displays moves of a pokemon of a certain generation"""


    resp = requests.get(f"{base_api}/pokemon/{pokemon}")

    pokemon = resp.json()
    moves = pokemon["moves"]

    if version == 'red' or version == 'blue':
        version = 'red-blue'
    if version == 'gold' or version == 'silver':
        version = 'gold-silver'
    if version == 'ruby' or version == 'sapphire':
        version = 'ruby-sapphire'
    if version == 'firered' or version == 'leafgreen':
        version = 'firered-leafgreen'
    if version == 'diamond' or version == 'pearl':
        version == 'diamond-pearl'
    if version == 'white' or version == 'black':
        version = 'black-white'
    if version == 'x' or version == 'y':
        version = 'x-y'
    if version == 'sun' or version == 'moon':
        version = 'sun-moon'
    if version == 'omega-ruby' or version == 'alpha-sapphire':
        version = 'omega-ruby-alpha-sapphire'
    if version == 'scarlet' or version == 'violet':
        version = 'scarlet-violet'
    if version == 'sword' or version == 'shield':
        version = 'sword-shield'
    if version == 'heartgold' or version == 'soulsilver':
        version = 'heartgold-soulsilver'
    if version == 'brilliant-diamond' or version == 'shining-pearl':
        version = 'brilliant-diamond-and-shining-pearl'
    if version == "ultra-sun" or version == ' ultra-moon':
        version = "ultra-sun-ultra-moon"
    if version == 'lets-go-pikachu' or version == 'lets-go-eevee':
        version == 'lets-go-pikachu-lets-go-eevee'
    if version == 'black-2' or version == 'white-2':
        version = 'black-2-white-2'



    
    return render_template("pokemon_moves.html", pokemon = pokemon, moves = moves, version = version)

@app.route("/moves")
def display_move_page():
        """Display moves base page"""

        resp = requests.get(f"{base_api}/type")
        types = resp.json()["results"]
    

        return render_template("moves.html", types = types)

@app.route("/moves/search")
def search_move():
    """Search for specific move"""

    move = requests.args("move")

    resp = requests.get(f"{base_api}/move/{move}")

    found_move = resp.json()["results"]
    

    if resp.status_code == 200:

        return render_template("move_info.html", move = found_move)

    else:
        return redirect ("/move", error = "Move not found")

@app.route("/moves/type/<type>")
def display_move_type_page(type):
    """Get and display data for type page"""

    resp = requests.get(f"{base_api}/type/{type}")

    moves = resp.json()['moves']

    return render_template("move_type.html", moves = moves)

@app.route('/moves/<move>')
def display_move_info(move):
    """Displays information on a move"""

    resp = requests.get(f"{base_api}/move/{move}")

    move = resp.json()

    return render_template('move_info.html', move = move)


@app.route('/items')
def display_item_page():
    """Display item home page"""

    return render_template("item.html")

@app.route('/items/<int:item_id>')
def item_info_page(item_id):
    """Finds and presents specific item info"""

    resp = requests.get(f"{base_api}/item/{item_id}")

    item = resp.json()
    held_by = len(item['held_by_pokemon'])

    return render_template('item_info.html', item = item, held_by = held_by)

@app.route('/users/<int:user_id>')
def display_user(user_id):


    user = User.query.get_or_404(user_id)


    teams =     (Teams
                .query
                .filter(Teams.user_id == user_id)
                .limit(100)
                .all())
    return render_template('user.html', user=user, teams = teams)

@app.route('/teams/new', methods = ["GET", "POST"])
def create_new_team():
    """Create new team
    Get form on GET submit form on POST"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    resp = requests.get(f"{base_api}/generation")
    gen = resp.json()["results"]
    
    form = TeamForm()
    form.gen.choices = [(gn['name'],gn['name']) for gn in gen]



    if form.validate_on_submit():
        team = Teams(name =form.name.data , gen = form.gen.data)
        g.user.teams.append(team)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('team_form.html', form=form)

@app.route('/teams/<int:team_id>')
def display_team(team_id):

    team = Teams.query.get_or_404(team_id)
    if g.user.id is not team.user_id:
        flash("Access Denied", 'danger')
        return redirect ('/')


    
    if len(team.pokemon)<6:
        add_ok = True
    else:
        add_ok = False
    return render_template("team.html", team = team, add_ok = add_ok)

@app.route('/teams/<int:team_id>/add', methods = ["GET", "POST"])
def select_pokemon(team_id):
    """Selects pokemon to add"""


    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    team = Teams.query.get_or_404(team_id)
    form = PokemonForm()
    form.pokemon.choices = []
    if team.gen == "generation-i":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
    
    elif team.gen == "generation-ii":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))

    elif team.gen == "generation-iii":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))

    elif team.gen == "generation-iv":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))

    elif team.gen == "generation-v":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/5")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))

    elif team.gen == "generation-vi":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/5")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/6")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
    
    elif team.gen == "generation-vii":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/5")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/6")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/7")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))

    elif team.gen == "generation-viii":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/5")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/6")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/7")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/8")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
    
    elif team.gen == "generation-ix":
        resp = requests.get(f"{base_api}/generation/1")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/2")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/3")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/4")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/5")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/6")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/7")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/8")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
        resp = requests.get(f"{base_api}/generation/9")
        pokemon = resp.json()['pokemon_species']
        for pkm in pokemon:
            form.pokemon.choices.append((pkm['name'], pkm['name']))
    
    form.pokemon.choices.sort()
    if form.validate_on_submit():
        pokemon = form.pokemon.data

        return redirect(f"/teams/{team.id}/add/{pokemon}")

    return render_template('pokemon_form.html', form=form)

@app.route('/teams/<int:team_id>/delete', methods = ["POST"])
def delete_team(team_id):
    '''Deletes chosen team'''
    
    team = Teams.query.get_or_404(team_id)
    if g.user.id is not team.user_id:
        flash("Access Denied", 'danger')
        return redirect ('/')
    
    g.user.teams.remove(team)
    db.session.commit()

    return redirect(f'/users/{g.user.id}')


@app.route("/teams/<int:team_id>/add/<pokemon>", methods = ["GET", "POST"])
def pokemon_details_form(team_id, pokemon):
    """Grabs and submits pokemon detail form"""

    team = Teams.query.get_or_404(team_id)
    resp = requests.get(f"{base_api}/pokemon/{pokemon}")
    abilities = resp.json()['abilities']
    moves = resp.json()['moves']
    gen = team.gen
    form = PokemonDetailForm()
    form.nature.choices = [('adamant', 'adamant'),('bashful', 'bashful'), ('bold', 'bold'), ('brave', 'brave'), ('calm', 'calm'), ('careful', 'careful'), ('docile', 'docile'),
    ('gentle', 'gentle'), ('hardy', 'hardy'), ("hasty", 'hasty'), ('impish', 'impish'), ('jolly', 'jolly'), ('lax', 'lax'), ('lonely', 'lonely'),('mild', 'mild'),
    ('modest', 'modest'), ('naive', 'naive'), ('naughty', 'naughty'), ('quiet', 'quiet'), ('quirky', 'quirky'), ('rash', 'rash'), ('relaxed', 'relaxed'), ('sassy', 'sassy'),
    ('serious', 'serious'), ('timid','timid')]
    form.ability.choices = [(a['ability']['name'],a['ability']['name'] ) for a in abilities]
    move_choices  = []
    if gen == 'generation-i':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'red-blue' or game['version_group']['name'] == 'yellow':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-ii':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'gold-silver' or game['version_group']['name'] == 'crystal':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-iii':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'ruby-sapphire' or game['version_group']['name'] == 'emerald':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-iv':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'diamond-pearl' or game['version_group']['name'] == 'platinum':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-v':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'black-white' or game['version_group']['name'] == 'black-2-white-2':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-vi':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'x-y':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-vii':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'sun-moon':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-viii':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'sword-shield':
                    move_choices.append((move['move']['name'], move['move']['name']))

    elif gen == 'generation-ix':
        for move in moves:
            for game in move['version_group_details']:
                if game['version_group']['name'] ==  'scarlet-violet':
                    move_choices.append((move['move']['name'], move['move']['name']))

    move_choices.sort()

    form.move_1.choices = move_choices
    form.move_2.choices = move_choices
    form.move_3.choices = move_choices
    form.move_4.choices = move_choices

    if form.validate_on_submit():

        new_pokemon = Pokemon(name= pokemon, nature = form.nature.data, abilities = form.ability.data, move_one = form.move_1.data, 
        move_two =form.move_2.data, move_three =form.move_3.data, move_four = form.move_4.data )

        team.pokemon.append(new_pokemon)
        db.session.commit()

        return redirect(f"/teams/{team.id}")

    return render_template("pokemon_detail_form.html", form = form)

@app.route('/teams/<int:team_id>/pokemon/<int:pokemon_id>/delete', methods = ["POST"])
def delete_pokemon(team_id, pokemon_id):

    team = Teams.query.get_or_404(team_id)
    if g.user.id is not team.user_id:
        flash("Access Denied", 'danger')
        return redirect ('/')

    pokemon = Pokemon.query.get_or_404(pokemon_id) 
    team.pokemon.remove(pokemon)
    db.session.commit()   

    return redirect(f'/teams/{team.id}')      
