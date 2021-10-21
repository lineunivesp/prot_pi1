from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    company = StringField('Empresa', validators=[DataRequired()])
    content = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Publicar!')