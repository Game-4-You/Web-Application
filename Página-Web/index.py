import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

data_file_path = os.path.join(os.path.dirname(__file__), 'server', 'data.json')

with open(data_file_path) as f:
    users = json.load(f)


@app.route('/data')
def get_data():
    with open('server/data.json') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Buscar el usuario en la lista de usuarios
        for user in users:
            if user['Username'] == username and user['UserID'] == password:
                return redirect(url_for('home'))

        return "Nombre de usuario o contraseña incorrectos", 401
    else:
        return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
