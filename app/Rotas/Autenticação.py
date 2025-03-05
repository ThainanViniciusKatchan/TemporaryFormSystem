from app import app
from flask import render_template, redirect, session, url_for, request


# Rota para redirecionamento da rota / para /OAuth/Login automáticamente
@app.route('/')
def index():
    return redirect(url_for('LoginUser'))


# Rota que mostra as opções de logín para o usuário
@app.route('/OAuth/Login', methods=['GET'])
def LoginUser():
    return render_template('Login.html')


@app.route('/OAuth/Cadastrar', methods=['GET', 'POST'])
def CadastrarUser():
    return ...


@app.route('/OAuth/Logout', methods=['GET'])
def LogoutUser():
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))
    session.clear()
    return redirect(url_for('LoginUser'))
