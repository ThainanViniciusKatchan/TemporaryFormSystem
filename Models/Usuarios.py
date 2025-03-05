from app import app, Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dataclasses import dataclass


login_manager = LoginManager(app)

bcrypt = Bcrypt(app)
bcrypt.init_app(app)


# classe para criação da tabela 'usuario' no banco de dados
@dataclass
class Usuario(Config.db.Model):
    __tablename__ = 'usuario'
    User_id = Config.db.Column(Config.db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Config.db.Column(Config.db.String(100), nullable=False)
    email = Config.db.Column(Config.db.String(250), nullable=False)
    senha = Config.db.Column(Config.db.String(80), nullable=False)
    token = Config.db.Column(Config.db.Text, nullable=False)
    refresh_token = Config.db.Column(Config.db.Text, nullable=True)

    Token = Config.db.relationship('Token', backref='usuario', lazy=True)

    def __init__(self, nome, email, senha, token, refresh_token, **kwargs):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.token = token
        self.refresh_token = refresh_token
        super().__init__(**kwargs)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


with app.app_context():
    Config.db.create_all()
