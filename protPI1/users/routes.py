from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from protPI1 import db, bcrypt
from protPI1.models import User, Post
from protPI1.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from protPI1.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

#Registrar Usuário (Provavelmente será retirado do principal)
@users.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('users.register'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, nome=form.first_name.data, sobrenome=form.last_name.data, email=form.email.data, senha=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('A conta foi criada! O novo usuário já pode logar!', 'success')
        return redirect(url_for('users.register'))
    return render_template('register.html', title='Registrar', form=form)


# Página de Login (Admin only)
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login inválido. Favor checar username e senha!', 'danger')
    return render_template('login.html', title='Login', form=form)


# Dar logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Atualizar Dados do Usuário
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.imgfile = picture_file
        current_user.username = form.username.data
        current_user.nome = form.first_name.data
        current_user.sobrenome = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Perfil atualizado!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.nome
        form.last_name.data = current_user.sobrenome
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.imgfile)
    return render_template('account.html', title='Perfil', image_file=image_file, form=form)


# Página do autor e seus posts   (externos)
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.data_post.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', title=f'Publicações de {user.username}', posts=posts, user=user)


# Redefinir senha  1 - email
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     form = RequestResetForm()
     if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Um email foi enviado com instruções para redefinir sua senha.', 'info')
        return redirect(url_for('users.login'))
     return render_template('reset_request.html', title='Reset Password', form=form)


# Redefinir senha 2 - senha
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
     if current_user.is_authenticated:
         return redirect(url_for('main.home'))
     user = User.verify_reset_token(token)
     if user is None:
         flash('Este é um token inválido ou expirado', 'warning')
         return redirect(url_for('users.reset_request'))
     form = ResetPasswordForm()
     if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user.senha = hashed_password
         db.session.commit()
         flash('Sua senha foi atualizada! Agora você está apto para logar!', 'success')
         return redirect(url_for('users.login'))
     return render_template('reset_token.html', title='Reset Password', form=form)