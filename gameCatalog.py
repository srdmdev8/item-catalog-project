from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Console, ConsoleGame, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Game Catalog"

engine = create_engine('sqlite:///consolegames.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect from Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace the
        remaining quotes with nothing so that it can be used directly in the
        graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = \
        'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<div class="loginStatus">'
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    output += '</div>'

    flash("You are now logged in as %s" % login_session['username'])
    return output


# Disconnect from Facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' \
        % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Connect from Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<div class="loginStatus">'
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    output += '</div>'
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect from Google - Revoke a current user's token and reset their
# login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for \
            given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Console Games JSON
@app.route('/consoles/<int:console_id>/games/JSON')
def consoleGamesJSON(console_id):
    '''
    Render JSON of all games for specified console.
    '''
    console = session.query(Console).filter_by(id=console_id).one()
    games = session.query(ConsoleGame).filter_by(
        console_id=console_id).all()
    return jsonify(Console=[i.serialize for i in games])


# Game JSON
@app.route('/consoles/<int:console_id>/games/<int:game_id>/JSON')
def gameJSON(console_id, game_id):
    '''
    Render JSON of specific game.
    '''
    game = session.query(ConsoleGame).filter_by(id=game_id).one()
    return jsonify(ConsoleGame=game.serialize)


# Consoles JSON
@app.route('/consoles/JSON')
def consolesJSON():
    '''
    Render JSON of all consoles.
    '''
    consoles = session.query(Console).all()
    return jsonify(consoles=[console.serialize for console in consoles])


# Show all consoles
@app.route('/')
@app.route('/consoles/')
@app.route('/consoles')
def showConsoles():
    '''
    Query all consoles and list them on HTML template in ascending order based
    on console name. Also, verify the user's login status to determine which
    version of the console page they see.
    '''
    console = session.query(Console).order_by(asc(Console.name))
    if 'username' not in login_session:
        return render_template('publicconsoles.html', console=console)
    else:
        return render_template('consoles.html', console=console)


# Add new console
@app.route('/consoles/new', methods=['GET', 'POST'])
def newConsole():
    '''
    First verify login status and redirect to login page as needed.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    '''
    If the user adds a new console via the POST method, get the value of the
    new name, initialize the creator, add/commit the new console to the
    database and provide a flash message on the redirect screen.
    '''
    if request.method == 'POST':
        newConsole = Console(name=request.form['name'],
                             user_id=login_session['user_id'])
        session.add(newConsole)
        session.commit()
        flash("New Console Created!")
        return redirect(url_for('showConsoles'))
    else:
        '''
        Render the template for adding a new console.
        '''
        return render_template('newconsole.html')


# Edit console
@app.route('/consoles/<int:console_id>/edit', methods=['GET', 'POST'])
def editConsole(console_id):
    '''
    Set the console that is being edited and then verify the login status of
    the user and redirect to login page as needed.
    '''
    editedConsole = session.query(Console).filter_by(id=console_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    '''
    If the console being edited was not created by the user, display message
    that they are not authroized to perform this action.
    '''
    if editedConsole.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized" \
        "to edit this Console. Please create your own console in order to " \
        "edit.');}</script><body onload='myFunction()'>"
    '''
    If the user edits a console via the POST method, get the value of the
    updated name, add/commit that name to the
    database and provide a flash message on the redirect screen.
    '''
    if request.method == 'POST':
        if request.form['name']:
            editedConsole.name = request.form['name']
        session.add(editedConsole)
        session.commit()
        flash("Console Successfully Edited!")
        return redirect(url_for('showConsoles'))
    else:
        '''
        Render the template for editing a console.
        '''
        return render_template('editconsole.html', i=editedConsole)


# Delete console
@app.route('/consoles/<int:console_id>/delete', methods=['GET', 'POST'])
def deleteConsole(console_id):
    '''
    Set the console that is being deleted and then verify the login status of
    the user and redirect to login page as needed.
    '''
    consoleToDelete = session.query(Console).filter_by(id=console_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    '''
    If the console being deleted was not created by the user, display message
    that they are not authroized to perform this action.
    '''
    if consoleToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized" \
        "to delete this console. Please create your own console in order to " \
        "delete.');}</script><body onload='myFunction()'>"
    '''
    If the user deletes a console via the POST method, delete the specific
    console and commit to the database. Then provide a flash message on the
    redirect screen.
    '''
    if request.method == 'POST':
        session.delete(consoleToDelete)
        session.commit()
        flash("Console Successfully Deleted!")
        return redirect(url_for('showConsoles'))
    else:
        '''
        Render the template for deleting a console.
        '''
        return render_template('deleteconsole.html', i=consoleToDelete)


# Show games for console
@app.route('/consoles/<int:console_id>/')
@app.route('/consoles/<int:console_id>')
@app.route('/consoles/<int:console_id>/games')
@app.route('/consoles/<int:console_id>/games/')
def consoleGames(console_id):
    '''
    Query console by id and query for all games listed for that console to
    display on HTML template. Then, verify the user's login status to determine
    which version of the console page they see.
    '''
    console = session.query(Console).filter_by(id=console_id).one()
    games = session.query(ConsoleGame).filter_by(console_id=console.id)
    if 'username' not in login_session:
        return render_template('publicgames.html', console=console,
                               games=games)
    else:
        return render_template('games.html', console=console, games=games)


# Add a new game
@app.route('/consoles/<int:console_id>/games/new', methods=['GET', 'POST'])
def newGame(console_id):
    '''
    First verify login status and redirect to login page as needed.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    '''
    If the console being deleted was not created by the user, display message
    that they are not authroized to perform this action.
    '''
    console = session.query(Console).filter_by(id=console_id).one()
    if login_session['user_id'] != console.user_id:
        return "<script>function myFunction() {alert('You are not authorized" \
        " to add games to this console. Please create your own console in " \
        "order to add games.');}</script><body onload='myFunction()'>"
    '''
    If the user adds a new console via the POST method, get the value of the
    inputs, add/commit the new game to the
    database and provide a flash message on the redirect screen.
    '''
    if request.method == 'POST':
        newGame = ConsoleGame(
            name=request.form['name'], description=request.form['description'],
            price=request.form['price'], publisher=request.form['publisher'],
            console_id=console_id, user_id=console.user_id)
        session.add(newGame)
        session.commit()
        flash("New Game Created!")
        return redirect(url_for('consoleGames', console_id=console_id))
    else:
        '''
        Render the template for adding a new game.
        '''
        return render_template('newgame.html', console_id=console_id)


# Edit a game
@app.route('/consoles/<int:console_id>/games/<int:game_id>/edit',
           methods=['GET', 'POST'])
def editGame(console_id, game_id):
    '''
    Verify the login status of the user and redirect to login page as needed.
    Then, set the game that is being edited and the console the game is for.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    editedGame = session.query(ConsoleGame).filter_by(id=game_id).one()
    console = session.query(Console).filter_by(id=console_id).one()
    '''
    If the console of the game being edited was not created by the user,
    display message that they are not authroized to perform this action.
    '''
    if login_session['user_id'] != console.user_id:
        return "<script>function myFunction() {alert('You are not authorized" \
        " to edit games for this console. Please create your own console in " \
        "order to edit games.');}</script><body onload='myFunction()'>"
    '''
    If the user edits a game via the POST method, get the value of the
    inputs, add/commit the updates to the database and provide a flash message
    on the redirect screen.
    '''
    if request.method == 'POST':
        if request.form['name']:
            editedGame.name = request.form['name']
        if request.form['description']:
            editedGame.description = request.form['description']
        if request.form['price']:
            editedGame.price = request.form['price']
        if request.form['publisher']:
            editedGame.publisher = request.form['publisher']
        session.add(editedGame)
        session.commit()
        flash("Game Successfully Edited!")
        return redirect(url_for('consoleGames', console_id=console_id))
    else:
        '''
        Render the template for editing a game.
        '''
        return render_template(
            'editgame.html', console_id=console_id, game_id=game_id,
            i=editedGame)


# Delete a game
@app.route('/consoles/<int:console_id>/games/<int:game_id>/delete',
           methods=['GET', 'POST'])
def deleteGame(console_id, game_id):
    '''
    Verify the login status of the user and redirect to login page as needed.
    Then, set the game that is being deleted and the console the game is for.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    console = session.query(Console).filter_by(id=console_id).one()
    gameToDelete = session.query(ConsoleGame).filter_by(id=game_id).one()
    '''
    If the console of the game being deleted was not created by the user,
    display message that they are not authroized to perform this action.
    '''
    if login_session['user_id'] != console.user_id:
        return "<script>function myFunction() {alert('You are not authorized" \
        " to delete games from this console. Please create your own console " \
        "in order to delete games.');}</script><body onload='myFunction()'>"
    '''
    If the user deletes a game via the POST method, delete the specific
    game and commit to the database. Then provide a flash message on the
    redirect screen.
    '''
    if request.method == 'POST':
        session.delete(gameToDelete)
        session.commit()
        flash("Game Successfully Deleted!")
        return redirect(url_for('consoleGames', console_id=console_id))
    else:
        '''
        Render the template for deleting a game.
        '''
        return render_template(
            'deletegame.html', i=gameToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    '''
    If provider exists, determine whether google or facebook. Then disconnect
    accordingly and redirect user to the console page.
    '''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showConsoles'))
    else:
        '''
        Render the template for the consoles page and display a flash message.
        '''
        flash("You were not logged in")
        return redirect(url_for('showConsoles'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
