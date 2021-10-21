import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# local server
app = Flask(__name__)
# bd
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# encrypt
bcrypt = Bcrypt(app)
# login messages
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Favor logar para acessar esta página!"
login_manager.login_message_category = 'info'
# email sender
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'um gmail teste, evitar o seu gmail pessoal'
app.config['MAIL_PASSWORD'] = 'a senha desse gmail'
mail = Mail(app)

from protPI1 import routes