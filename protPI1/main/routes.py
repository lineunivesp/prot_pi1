from flask import render_template, request, Blueprint
from protPI1.models import Post

main = Blueprint('main', __name__)


# Página Principal
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_post.desc()).paginate(page=page ,per_page=5)
    return render_template('home.html', posts=posts)


# Página dos Contatinhos, do Quem Somos, do O que é o projeto
@main.route("/about")
def about():
    return render_template('about.html', title='Sobre nós')