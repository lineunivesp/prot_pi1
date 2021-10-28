from datetime import datetime
from flask import current_app
from protPI1 import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    sobrenome = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    imgfile = db.Column(db.String(20), nullable=False, default='default.jpg')
    senha = db.Column(db.String(75), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.nome}', '{self.sobrenome}', '{self.email}', '{self.imgfile}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(50), nullable=False)
    data_post = db.Column(db.DateTime, nullable=False, default=datetime.now)
    descricao = db.Column(db.Text, nullable=False)
    tipo_post = db.Column(db.String(7), nullable=False)
    cidade = db.Column(db.String(75), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    nivel_vaga = db.Column(db.String(20), nullable=True)
    nivel_curso = db.Column(db.String(20), nullable=True)
    mod_vaga = db.Column(db.String(20), nullable=True)
    mod_curso = db.Column(db.String(20), nullable=True)
    link = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    user_emp = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.titulo}', '{self.empresa}', '{self.data_post}, '{self.descricao}', '{self.tipo_post}" \
               f", '{self.cidade}, '{self.estado}, '{self.nivel_vaga}, '{self.nivel_curso}, '{self.mod_vaga}" \
               f", '{self.mod_curso}, '{self.link})"

#class Empresa(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    nome = db.Column(db.String(100), nullable=False)
#    descricao = db.Column(db.String(100), nullable=False)
#    eposts = db.relationship('Empresa', backref='empresa', lazy=True)

#    def __repr__(self):
#        return f"Post('{self.nome}', '{self.empdesc}')"