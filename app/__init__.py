import os.path
import traceback
from flask import Flask


templates = os.path.join(os.getcwd(), 'templates')
static = os.path.join(os.getcwd(), 'static')

# Ignora a necessidade de https:// para autenticação do Google com OAuth2
"""use isso somente em desenvolvimento quando colocar em produção retire essa linha"""
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__, template_folder=templates, static_folder=static)

# Caminho para o arquivo credentials.json
CLIENT_SECRETS_FILE = 'app/credentials.json'

# Escopos necessários (inclui permissão para enviar e-mails)
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email",
          "https://www.googleapis.com/auth/userinfo.profile",
          "https://www.googleapis.com/auth/gmail.send"]

# URL de redirecionamento após a autenticação
REDIRECT_URI = 'http://127.0.0.1:8000/callback'

# Caso as rotas não se íniciem aparecera uma mensagem de erro no terminal
try:
    from app.Rotas import formulario, PDF, OAuth2, Test, Autenticação, DashBoard
except ImportError:
    print("Erro ao inciar as rotas")
    print(traceback.format_exc())

