from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import current_user
from blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Abbonati(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    scadenza = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    cell = db.Column(db.String(20), nullable=False)
    quota = db.Column(db.Integer, nullable=False)
    versato = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(100), nullable=False, default='')
    end_near = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"Abbonati('{self.nome}', '{self.scadenza}', '{self.cell}', '{self.quota}', '{self.versato}', '{self.note}')"


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()