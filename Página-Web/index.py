import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import secrets
import requests
from pymongo import MongoClient

client = MongoClient('mongodb+srv://fabritzziopescoran:oZRbG4bYRYEldXmU@game4udata.duy9eaj.mongodb.net/')

db = client['Game4U']
collection = db['user-videogame-dataset']

users = list(collection.find())
for user in users:
    user['_id'] = str(user['_id'])

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# Define la función para obtener la URL de la imagen
def get_image_url(game_name):
    api_key = 'AIzaSyCDdtNae_OIMvga8-Csy-yvkxQ74o-WmOU'
    search_engine_id = '763dfea0c13cf4b9a'
    search_url = f"https://www.googleapis.com/customsearch/v1?q={game_name}&searchType=image&key={api_key}&cx={search_engine_id}"

    response = requests.get(search_url)
    results = response.json()

    if 'items' in results and len(results['items']) > 0:
        return results['items'][0]['link']
    else:
        return url_for('static', filename='assets/default_image.jpg')


def get_friends_games(user):
    friends_games = []
    for friend_id in user['Friends']:
        for friend in users:
            if friend['UserID'] == friend_id:
                friends_games.append({'Username': friend['Username'], 'Games': friend['Games']})
                break
    return friends_games


@app.route('/data')
def get_data():
    with open('server/data.json') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/')
def initial():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    # Agrega la URL de la imagen a cada juego
    for game in user['Games']:
        game['ImageUrl'] = get_image_url(game['Name'])

    # Obtener los juegos de los amigos
    friends_games = get_friends_games(user)

    for friend in friends_games:
        for game in friend['Games']:
            game['ImageUrl'] = get_image_url(game['Name'])

    return render_template('home.html', user=user, friends_games=friends_games)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Buscar el usuario en la lista de usuarios
        for user in users:
            if user['Username'] == username and user['UserID'] == password:
                # Guardar la información del usuario en la sesión
                session['user'] = user
                return redirect(url_for('home'))

        return "Nombre de usuario o contraseña incorrectos", 401
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        correo = request.form.get('correo')
        password = request.form.get('password')
        return redirect(url_for('specifications_register'))

    return render_template('register.html')


@app.route('/specifications_register')
def specifications_register():
    if request.method == 'POST':
        combo1 = request.form.get('combo1')
        combo2 = request.form.get('combo2')
        combo3 = request.form.get('combo3')
        combo4 = request.form.get('combo4')
        combo5 = request.form.get('combo5')

        return redirect(url_for('preferences_register'))

    return render_template('specifications_register.html')

@app.route('/preferences_register')
def preferences_register():
    return render_template('preferences_register.html')



@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/sales')
def sales():
    return render_template('sales.html')


@app.route('/free')
def free():
    return render_template('free.html')


@app.route('/subscription')
def subscription():
    return render_template('subscription.html')


if __name__ == '__main__':
    debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
