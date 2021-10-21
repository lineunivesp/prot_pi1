from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from protPI1 import db
from protPI1.models import Post
from protPI1.posts.forms import PostForm


posts = Blueprint('posts', __name__)


# Publicações (CRUD)
# CREATE (Criar nova publicação)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(titulo=form.title.data, empresa=form.company.data, descricao=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Nova Publicação', form=form, legend='Nova Publicação')


# Abrir página do posts selecionado
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.titulo, post=post)


# Atualizar posts
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.title.data
        post.empresa = form.company.data
        post.descricao = form.content.data
        db.session.commit()
        flash('Publicação atualizada!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.titulo
        form.company.data = post.empresa
        form.content.data = post.descricao
    return render_template('create_post.html', title='Atualizar Publicação', form=form, legend='Atualizar Publicação')


# Deletar Post
@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Publicação removida!', 'success')
    return redirect(url_for('main.home'))