from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Console, ConsoleGame

app = Flask(__name__)

engine = create_engine('sqlite:///consolegames.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Restaurant Menu JSON
@app.route('/consoles/<int:console_id>/games/JSON')
def consoleGamesJSON(console_id):
    console = session.query(Console).filter_by(id=console_id).one()
    games = session.query(ConsoleGame).filter_by(
        console_id=console_id).all()
    return jsonify(Console=[i.serialize for i in games])


#Menu Item JSON
@app.route('/consoles/<int:console_id>/games/<int:game_id>/JSON')
def menuItemJSON(console_id, game_id):
    game = session.query(ConsoleGame).filter_by(id=game_id).one()
    return jsonify(ConsoleGame=game.serialize)


#Show consoles
@app.route('/')
@app.route('/consoles/')
@app.route('/consoles')
def showConsoles():
    console = session.query(Console).all()
    return render_template('consoles.html', console=console)


#Add new console
@app.route('/consoles/new', methods=['GET', 'POST'])
def newConsole():
    if request.method == 'POST':
        newConsole = Console(name=request.form['name'])
        session.add(newConsole)
        session.commit()
        flash("New Console Created!")
        return redirect(url_for('showConsoles'))
    else:
        return render_template('newconsole.html')


#Edit console
@app.route('/consoles/<int:console_id>/edit', methods=['GET', 'POST'])
def editConsole(console_id):
    editedConsole = session.query(Console).filter_by(id=console_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedConsole.name = request.form['name']
        session.add(editedConsole)
        session.commit()
        flash("Console Successfully Edited!")
        return redirect(url_for('showConsoles'))
    else:
        return render_template('editconsole.html', i = editedConsole)


#Delete console
@app.route('/consoles/<int:console_id>/delete', methods=['GET', 'POST'])
def deleteConsole(console_id):
    consoleToDelete = session.query(Console).filter_by(id=console_id).one()
    if request.method == 'POST':
        session.delete(consoleToDelete)
        session.commit()
        flash("Console Successfully Deleted!")
        return redirect(url_for('showConsoles'))
    else:
        return render_template('deleteconsole.html', i = consoleToDelete)
    


#Show games for console
@app.route('/consoles/<int:console_id>/')
@app.route('/consoles/<int:console_id>')
@app.route('/consoles/<int:console_id>/games')
@app.route('/consoles/<int:console_id>/games/')
def consoleGames(console_id):
    console = session.query(Console).filter_by(id=console_id).one()
    games = session.query(ConsoleGame).filter_by(console_id=console.id)
    return render_template('games.html', console=console, games=games)


#Add a new game
@app.route('/consoles/<int:console_id>/games/new', methods=['GET', 'POST'])
def newGame(console_id):
    if request.method == 'POST':
        newGame = ConsoleGame(
            name=request.form['name'], console_id=console_id)
        session.add(newGame)
        session.commit()
        flash("New Game Created!")
        return redirect(url_for('consoleGames', console_id=console_id))
    else:
        return render_template('newgame.html', console_id=console_id)


#Edit a game
@app.route('/consoles/<int:console_id>/games/<int:game_id>/edit',
           methods=['GET', 'POST'])
def editGame(console_id, game_id):
    editedGame = session.query(ConsoleGame).filter_by(id=game_id).one()
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
        return render_template(
            'editgame.html', console_id=console_id, game_id = game_id, i = editedGame)


#Delete a game
@app.route('/consoles/<int:console_id>/games/<int:game_id>/delete',
           methods=['GET', 'POST'])
def deleteGame(console_id, game_id):
    gameToDelete = session.query(ConsoleGame).filter_by(id=game_id).one()
    if request.method == 'POST':
        session.delete(gameToDelete)
        session.commit()
        flash("Game Successfully Deleted!")
        return redirect(url_for('consoleGames', console_id=console_id))
    else:
        return render_template(
            'deletegame.html', i = gameToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
