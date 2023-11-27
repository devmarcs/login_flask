from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext import mysql
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User


app = Flask(__name__)
csrf = CSRFProtect()
db = mysql(app)
login_manager_app = LoginManager(app)



@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login_cliente'))

@app.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        # Esse parâmetro 0 dentro de User é o ID, como não tenho ele coloco 0
        user = User(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
                
            else:
                flash("Password Inválido...")
        else:
            flash("Usuário não existe...")
        return redirect(url_for('login_cliente'))
    else:
        return render_template('auth/login.html')
    
@app.route('/logout')
def logout():
    logout_user()    
    return redirect(url_for('login_cliente'))


@app.route('/home')
@login_required
def home():
    return render_template('auth/home.html')


def status_401(error):
    return redirect(url_for('login_cliente'))

def status_404(error):
    return "<h1>Página não encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
