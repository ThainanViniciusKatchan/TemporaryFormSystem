from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer

# declaração das configurações necessárias para criação do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NomeDoBanco.sqlite3'
app.config['SECRET_KEY'] = ''
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db, render_as_batch=True)


# Iniciando o Serializer para criação de um token do link temporário
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


with app.app_context():
    db.create_all()
