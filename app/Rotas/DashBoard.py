from app import app, Config
from flask import render_template, request, redirect, url_for, send_file, abort, session
from Funcoes import Gerar_Token_Link, ListarDados
from Models import LinksGeneration, Files
from os import path, getcwd


@app.route('/DashBoard', methods=['GET', 'POST'])
def DashBoard():
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))
    action = request.form.get('action')

    if action == 'GerarLink':
        return redirect(url_for('DashBoardLink'))
    return render_template('DashBoard.html', action=action)


@app.route('/DashBoard/LinkGenerate', methods=['GET', 'POST'])
def DashBoardLink():
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))
    link, Creation_data = Gerar_Token_Link.gerar_token_link()  # Objeto para criação de token
    return redirect('/DashBoard/LinkList')


@app.route('/DashBoard/LinkList', methods=['GET', 'POST'])
def DashBoardLinkList():
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))
    Links = ListarDados.ListaDados.Links(LinksGeneration.Token.query.all())  # captura do bando de dados todos os links

    Table_Links = LinksGeneration.Token
    Table_File = Files.Files

    User_id = session.get('User_id')

    # Filtragem dos links e arquivos do usuário logado
    Infos = Config.db.session.query(Table_Links).join(Table_File).add_columns(Table_Links.id,
                                                                              Table_Links.token,
                                                                              Table_Links.Creation_data,
                                                                              Table_Links.is_used,

                                                                              Table_File.id,
                                                                              Table_File.Name,
                                                                              Table_File.User,
                                                                              Table_File.Date).filter(
        Table_Links.User_id == User_id).all()

    # Sistema de paginação
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Limite de 10 links por página
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(Infos) + per_page - 1) // per_page
    items_on_pages = Infos[start:end]

    return render_template('Links.html', Links=Links, Infos=Infos, User_id=User_id,

                           # Dados para paginação
                           Items=items_on_pages,
                           total_pages=total_pages,
                           page=page)


@app.route('/DashBoard/PDFFile/<id>/<Name>')
def DashBoardPDF(id, Name):
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))
    Filename = Files.Files.query.filter_by(id=id, Name=Name).first()

    if not Filename:
        abort(404, "Arquivo não encontrado no banco de dados.")

    folder = path.join(getcwd(), 'ArquivosPDF')
    file_path = path.join(folder, Name)

    print(f"Procurando arquivo: {file_path}")

    if not path.exists(file_path):
        Title = 'Arquivo não encontrado'
        Message = 'O arquivo Selecionado ainda não foi criado, espere o usuário preencher o formulário'
        isform = False
        return render_template('Erro.html', Title=Title, Message=Message, isform=isform)

    return send_file(file_path, mimetype='application/pdf')
