from app import app, Config
from flask_bcrypt import Bcrypt
from dataclasses import dataclass

bcrypt = Bcrypt(app)
bcrypt.init_app(app)


# classe para criação da tabela 'token' no banco de dados
@dataclass
class Token(Config.db.Model):
    __tablename__ = 'token'
    id = Config.db.Column(Config.db.Integer, primary_key=True, autoincrement=True, nullable=False)
    token = Config.db.Column(Config.db.String(100), nullable=False)
    Creation_data = Config.db.Column(Config.db.DateTime, nullable=False)
    is_used = Config.db.Column(Config.db.Boolean, nullable=True)

    Files_id = Config.db.Column(Config.db.Integer, Config.db.ForeignKey('files.id', name='fk_files_Token'),
                                nullable=False)

    User_id = Config.db.Column(Config.db.Integer, Config.db.ForeignKey('usuario.User_id', name='fk_user_id'),
                               nullable=False)

    def __init__(self, token, Creation_data, is_used, Files_id, User_id):
        self.token = token
        self.Creation_data = Creation_data
        self.is_used = is_used
        self.Files_id = Files_id
        self.User_id = User_id

    def __repr__(self):
        return f'<Token {self.token}, User {self.User_id}>'
