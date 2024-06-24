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
    api_key = 'AIzaSyARhpi1so6F94F7TVt6e4k6EB6UweaID3E'
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


@app.route('/preferences_register', methods=['GET', 'POST'])
def preferences_register():
    if request.method == 'POST':
        # Handle the POST request here
        # For example, you can get form data using request.form
        juegofav = request.form.get('juegofav')
        generofav = request.form.get('generofav')
        # Then you can save this data to your database
        # After handling the POST request, you can redirect the user to another page if needed
        return redirect(url_for('home'))
    else:
        # This is the original GET request handler
        return render_template('preferences_register.html')


@app.route('/explore')
def explore():
    # Aquí debes obtener las noticias de alguna fuente
    news = [
        {
            'image': 'https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/software/switch/70010000063714/fb30eab428df3fc993b41c76e20f72e4d76d49734d17d31996b5ab61c414b117',
            'headline': 'Nuevo lanzamiento de Zelda: Tears of the Kingdom',
            'description': 'La esperada secuela de Breath of the Wild ya está disponible y promete llevar a los jugadores a nuevas alturas con su mundo abierto y su emocionante narrativa.',
            'url': 'https://example.com/news1'
        },
        {
            'image': 'https://cdn.vox-cdn.com/thumbor/H5VFbYOWULXVSPIt37woZU9xnfc=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/24898768/video_games_2024_release_dates.jpg',
            'headline': 'E3 2024: Anunciados los próximos grandes títulos',
            'description': 'Durante la conferencia de E3 de este año, los desarrolladores han revelado emocionantes nuevos títulos que llegarán en 2024, incluyendo sorpresas y esperados retornos.',
            'url': 'https://example.com/news2'
        },
        {
            'image': 'https://static.cdprojektred.com/cms.cdprojektred.com/16x9_big/23f12c864022304aeaf05d8f760417d583a1602d-1280x720.jpg',
            'headline': 'Cyberpunk 2077 recibe una gran actualización',
            'description': 'CD Projekt Red ha lanzado una actualización masiva para Cyberpunk 2077, corrigiendo numerosos bugs y añadiendo contenido nuevo que mejora la experiencia del juego.',
            'url': 'https://example.com/news3'
        },
        {
            'image': 'https://www.pcgamesn.com/wp-content/sites/pcgamesn/2024/06/league-of-legends-new-champion-aurora-abilities.jpg',
            'headline': 'League of Legends introduce un nuevo campeón',
            'description': 'Riot Games ha revelado a su nuevo campeón, un guerrero místico con habilidades únicas que promete cambiar el meta del juego en la próxima temporada.',
            'url': 'https://example.com/news4'
        },
        {
            'image': 'data:image/jpeg;base64,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',
            'headline': 'Minecraft celebra su décimo aniversario con una actualización especial',
            'description': 'Mojang celebra una década de Minecraft con una actualización especial que incluye nuevas características, mobs y biomas, invitando a los jugadores a redescubrir el mundo cúbico.',
            'url': 'https://example.com/news5'
        }
    ]


    return render_template('explore.html', news=news)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/subscription')
def subscription():
    return render_template('subscription.html')


if __name__ == '__main__':
    debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
