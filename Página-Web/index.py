import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

with open('Server/data.json') as f:
    users = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')


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
    app.run(debug=True)
