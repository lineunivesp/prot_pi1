import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    company = StringField('Empresa', validators=[DataRequired()])
    content = TextAreaField('Descrição', validators=[DataRequired()])
    # post_type = StringField('Tipo de Publicação', validators=[DataRequired()])
    post_type = SelectField('Publicação Tipo', choices=[('vaga', 'Vaga'),('curso','Curso')])
    city = StringField('Cidade', validators=[DataRequired()])
    state = StringField('Estado', validators=[DataRequired()])
    #job_level = StringField('Nível da vaga')
    #course_level = StringField('Nível do curso')
    job_mod = StringField('Tipo da vaga')
    course_mod = StringField('Tipo do curso')
    job_level = SelectField('Nível da vaga', choices=[('','-- Nível da vaga --'),('aprendiz','Aprendiz'),('estagio','Estágio'),('trainee', 'Trainee'),('junior','Junior'),('pleno','Pleno'),('senior','Sênior')])
    course_level = SelectField('Nível do curso', choices=[('','-- Nível do curso --'),('iniciante','Iniciante'),('intermediario','Intermediário'),('avancado', 'Avançado')])
    job_mod = SelectField('Tipo da vaga', choices=[('','-- Tipo da vaga --'),('escritorio','Escritório'),('hibrido','Híbrido'),('homeoffice', 'Home Office')])
    course_mod = SelectField('Tipo do curso', choices=[('','-- Tipo do curso --'),('presencial','Presencial'),('semipresencial','Semipresencial'),('ead', 'EAD')])
    link = StringField('Link')
    submit = SubmitField('Publicar!')
