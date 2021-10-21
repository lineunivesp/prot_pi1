import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from protPI1 import mail


# Salvar imagem de perfil
# f_name = _
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_fn)
# transformado em i.save ->    form_picture.save(picture_path)
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# Enviar link de redefinição de senha pra email
def send_reset_email(user):
     token = user.get_reset_token()
     msg = Message('Solicitação de redefinição de senha', sender='noreply@demo.com', recipients=[user.email])
     msg.body = f'''Para redefinir sua senha, visite o seguinte link:
                        {url_for('users.reset_token', token=token, _external=True)}
                        Se você não fez esta solicitação, simplesmente ignore esta mensagem 
                        e nenhuma alteração será realizada. '''
     mail.send(msg)


