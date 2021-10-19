import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from protPI1 import app, db, bcrypt
from protPI1.forms import RegistrationForm, LoginForm, UpdateAccountForm
from protPI1.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'titulo': 'Desenvolvedor',
        'empresa': 'Line Data',
        'descricao': 'Precisa-se de devs bons e legais.',
        'data_post': '09 de outubro de 2021'
    },
    {
        'titulo': 'Operador de Suporte II',
        'empresa': 'LAB Comunicações',
        'descricao': 'Alguém pra fazer dar suporte pro cliente quando ele tiver dúvidas.',
        'data_post': '10 de outubro de 2021'
    },
    {
        'titulo': 'Admin. de Redes',
        'empresa': 'LAB Comunicações',
        'descricao': 'Alguém pra tomar conta da infra de redes da empresa ',
        'data_post': '10 de outubro de 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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