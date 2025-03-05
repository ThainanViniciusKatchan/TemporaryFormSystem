from flask import redirect, Response, render_template, request, session
from app import app, Config
import requests
from dataclasses import dataclass
from oauthlib.oauth2 import WebApplicationClient
from Models import Usuarios

# Colocar o client_id OAuth2 criado no Google Cloud aqui
# Put the OAuth2 client_id created in Google Cloud here
Google_Client_Id = ""

# Colocar aqui a Chave Secreta do cliente criado no Google Cloud aqui
# Place the Secret Key of the client created in Google Cloud here
Google_Secret = ""

oauth = WebApplicationClient(client_id=Google_Client_Id)


@dataclass
class GoogleHosts:
    authorization_endpoint: str
    token_endpoint: str
    user_info_endpoint: str
    certs: str


def get_google_oauth_Hosts() -> GoogleHosts:
    hosts = requests.get('https://accounts.google.com/.well-known/openid-configuration')

    if hosts.status_code != 200:
        raise Exception('Erro ao recuperar os endpoints de autenticação do Google.')

    data = hosts.json()

    return GoogleHosts(authorization_endpoint=data.get('authorization_endpoint'),
                       token_endpoint=data.get('token_endpoint'),
                       user_info_endpoint=data.get('userinfo_endpoint'),
                       certs=data.get('jwks_uri'))


# Rota de autenticação com o Google
# Rote of OAuth2 authentication
@app.route('/OAuth/LoginGoogle', methods=['GET'])
def OAuthLogin() -> Response:
    hosts = get_google_oauth_Hosts()

    """Mude o redirect_uri para a rota que está configurado no seu google cloud
    Change the redirect_uri to the route that is configured in your google cloud"""
    redirect_uri = oauth.prepare_request_uri(hosts.authorization_endpoint,
                                             redirect_uri='http://127.0.0.1:8000/callback',
                                             scope=['openid', 'email', 'profile',
                                                    'https://www.googleapis.com/auth/gmail.send'])

    return redirect(location=redirect_uri)


# Rota que recebe as informações do usuário de forma segura
# callBack rote
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    code = request.args.get('code')
    if not code:
        return "Erro: Código de autorização não recebido.", 400

    hosts = get_google_oauth_Hosts()

    """Mude o redirect_uri para a rota que está configurado no seu google cloud
    Change the redirect_uri to the route that is configured in your google cloud"""
    token_response = requests.post(
        hosts.token_endpoint,
        data={
            "code": code,
            "client_id": Google_Client_Id,
            "client_secret": Google_Secret,
            "redirect_uri": "http://127.0.0.1:8000/callback",
            "grant_type": "authorization_code"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if token_response.status_code != 200:
        return redirect('/OAuth/LoginGoogle')

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    session['access_token'] = access_token
    user_refresh_token = token_data.get("refresh_token")

    # Recupera as informações do usuário (incluindo o e-mail)
    userinfo_response = requests.get(
        hosts.user_info_endpoint,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if userinfo_response.status_code != 200:
        return f"Erro ao obter informações do usuário: {userinfo_response.text}", 400

    userinfo = userinfo_response.json()
    user_email = userinfo.get("email")
    session['user_email'] = user_email
    user_nome = userinfo.get("name")

    if not Usuarios.Usuario.query.filter_by(email=user_email).first():
        NovoUsuario = Usuarios.Usuario(nome=user_nome,
                                       senha='',
                                       email=user_email,
                                       token=access_token,
                                       refresh_token=user_refresh_token)

        Config.db.session.add(NovoUsuario)
        Config.db.session.commit()
    else:
        User = Usuarios.Usuario.query.filter_by(email=user_email).first()
        User.token = access_token
        if user_refresh_token:
            User.refresh_token = user_refresh_token

    session['EmailApi'] = Usuarios.Usuario.query.filter_by(email=user_email).first()
    User_Email = session.get('EmailApi')
    session['User_id'] = User_Email.User_id
    print(f'User: {session['User_id']}')

    return redirect("/DashBoard")
