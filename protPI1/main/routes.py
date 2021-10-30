from flask import render_template, request, Blueprint
from protPI1.models import Post


main = Blueprint('main', __name__)


# Página Principal
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_post.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/vagas")
def vagas():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(tipo_post = 'vaga').order_by(Post.data_post.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/cursos")
def cursos():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(tipo_post = 'curso').order_by(Post.data_post.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


# Página dos Contatinhos, do Quem Somos, do que é o projeto
@main.route("/about")
def about():
    return render_template('about.html', title='Sobre nós')