from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from protPI1.config import Config


# bd
db = SQLAlchemy()
# encrypt
bcrypt = Bcrypt()
# login messages
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = u"Favor logar para acessar esta página!"
login_manager.login_message_category = 'info'
# email sender
mail = Mail()


def create_app(config_class=Config):
    # local server
    app = Flask(__name__)
    # config
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from protPI1.users.routes import users
    from protPI1.posts.routes import posts
    from protPI1.main.routes import main
    from protPI1.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
