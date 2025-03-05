from app import app, Config
from dataclasses import dataclass


# classe para criação da tabela 'Files' no banco de dados
@dataclass
class Files(Config.db.Model):
    __tablename__ = 'files'

    id = Config.db.Column(Config.db.Integer, primary_key=True)

    Name = Config.db.Column(Config.db.String, nullable=True)
    User = Config.db.Column(Config.db.String, nullable=True)
    Date = Config.db.Column(Config.db.Date, nullable=True)

    Token = Config.db.relationship('Token', backref='files', lazy=True)

    def __init__(self, Name, User, Date):
        self.Name = Name
        self.User = User
        self.Date = Date

    def __repr__(self):
        return f'<{self.Name}: {self.User}>'

