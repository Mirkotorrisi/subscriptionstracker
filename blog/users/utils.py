import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def save_pic(form_picture):
    random_ex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_ex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return(picture_fn)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="blogdimirko@gmail.com", recipients = [user.email])
    msg.body = f'''Per resettare la password, segui questo link: {url_for('users.reset_token', token=token, _external=True)}

    Se non hai fatto questa richiesta, ignorala.'''
    mail.send(msg)
