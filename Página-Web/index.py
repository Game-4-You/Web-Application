import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import secrets
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

data_file_path = os.path.join(os.path.dirname(__file__), 'server', 'data.json')

with open(data_file_path) as f:
    users = json.load(f)


# Define la función para obtener la URL de la imagen
def get_image_url(game_name):
    api_key = 'AIzaSyBqSqoY28lVfmPC6w61vQT2P16SV9UXchw'
    search_engine_id = '763dfea0c13cf4b9a'
    search_url = f"https://www.googleapis.com/customsearch/v1?q={game_name}&searchType=image&key={api_key}&cx={search_engine_id}"

    response = requests.get(search_url)
    results = response.json()

    if 'items' in results and len(results['items']) > 0:
        return results['items'][0]['link']
    else:
        # URL de imagen predeterminada local
        return url_for('static', filename='assets/default_image.jpg')  # Asegúrate de tener esta imagen en la carpeta 'static/assets'

# Nueva función para obtener los juegos de los amigos
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
    return render_template('specifications_register.html')


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
