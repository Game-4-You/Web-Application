import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

data_file_path = os.path.join(os.path.dirname(__file__), 'server', 'data.json')

with open(data_file_path) as f:
    users = json.load(f)


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
    return render_template('home.html', user=user)


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


@app.route('/register')
def register():
    return render_template('register.html')


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
