from datetime import datetime
from protPI1 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    imgfile = db.Column(db.String(20), nullable=False, default='default.jpg')
    senha = db.Column(db.String(75), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.imgfile}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(50), nullable=False)
    data_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descricao= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    user_emp = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.titulo}', '{self.empresa}', '{self.data_post}')"

#class Empresa(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    nome = db.Column(db.String(100), nullable=False)
#    descricao = db.Column(db.String(100), nullable=False)
#    eposts = db.relationship('Empresa', backref='empresa', lazy=True)

#    def __repr__(self):
#        return f"Post('{self.nome}', '{self.empdesc}')"