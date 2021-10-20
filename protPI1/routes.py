import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from protPI1 import app, db, bcrypt
from protPI1.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from protPI1.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# Página Principal
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_post.desc()).paginate(page=page ,per_page=5)
    return render_template('home.html', posts=posts)


# Página dos Contatinhos, do Quem Somos, do O que é o projeto
@app.route("/about")
def about():
    return render_template('about.html', title='About')


#Registrar Usuário (Provavelmente será retirado do principal)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, senha=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Está apto para logar!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Página de Login (Admin only)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login inválido. Favor checar email e senha!', 'danger')
    return render_template('login.html', title='Login', form=form)


# Dar logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Salvar imagem de perfil
# f_name = _
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
# transformado em i.save ->    form_picture.save(picture_path)
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# Atualizar Dados do Usuário
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.imgfile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Perfil atualizado!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.imgfile)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# Publicações (CRUD)
# CREATE (Criar nova publicação)
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(titulo=form.title.data, empresa=form.company.data, descricao=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='Nova Publicação')

# Abrir página do post selecionado
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.titulo, post=post)

# Atualizar post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.titulo
        form.company.data = post.empresa
        form.content.data = post.descricao
    return render_template('create_post.html', title='Update Post', form=form, legend='Atualizar Publicação')

# Deletar Post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Publicação removida!', 'success')
    return redirect(url_for('home'))

# Página do autor e seus posts   (externos)
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.data_post.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)