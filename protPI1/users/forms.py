from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from protPI1.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, first_name, last_name):
        user_fn = User.query.filter_by(nome=first_name.data).first()
        user_ln = User.query.filter_by(sobrenome=last_name.data).first()
        if user_fn and user_ln:
            raise ValidationError('Este usuário já está registrado! Por favor, escolha outro!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Usuário registrado! Por favor, escolha outro!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está registrado! Por favor, escolha outro!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me!')
    submit = SubmitField('Logar!')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Atualizar avatar!', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar!')

    def validate_username(self, first_name, last_name):
        user_fn = User.query.filter_by(nome=first_name.data).first()
        user_ln = User.query.filter_by(sobrenome=last_name.data).first()
        if user_fn and user_ln:
            raise ValidationError('Este usuário já está registrado! Por favor, escolha outro!')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Usuário já está registrado! Por favor, escolha outro!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email já está registrado! Por favor, escolha outro!')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar redefinição de senha!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Não há conta neste email! Pracisa se registrar primeiro!.')

class ResetPasswordForm(FlaskForm):
     password = PasswordField('Senha', validators=[DataRequired()])
     confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
     submit = SubmitField('Redefinir senha!')