from app import app, Config
from playwright.sync_api import sync_playwright
import pathlib
import os
from flask import render_template, redirect, request, session, url_for
from Funcoes import data_convert, FormatarDocumentos, EnviarEmail
from datetime import datetime, date
from Models import Files, LinksGeneration


@app.route('/GerarPDF/<int:id>', methods=['GET', 'POST'])
def GerarPDF(id):
    if not 'User_id' in session:
        return redirect(url_for('LoginUser'))

    """ Variáveis que recebem os dados da URL """
    nome = request.args.get('NomeCompleto')
    # Formatação do CPF com pontos e travessão
    cpf = FormatarDocumentos.FomartDocumets.format_cpf(request.args.get('CPFCompleto'))
    # Formatação da data para o padrão do Brasil
    DataNascimento = data_convert.DataConverter.formatar(request.args.get('DataDeNascimento'))

    # Formatação do RG com pontos e travessão
    RG = FormatarDocumentos.FomartDocumets.Format_RG(request.args.get('RgCompleto'))
    EstadoCivil = request.args.get('EstadoCivil')
    OrgaoEmissor = request.args.get('OrgaoEmissor')
    # Formatação da data para o padrão do Brasil
    DataEmissao = data_convert.DataConverter.formatar(request.args.get('DataDeEmicaoRG'))

    # Formatar O número de telefone
    Telefone = FormatarDocumentos.FomartDocumets.Format_Tel(request.args.get('telefone'))
    Nacionalidade = request.args.get('Nacionalidade')
    LocalNascimento = request.args.get('LocalDeNascimento')
    Profissao = request.args.get('Profissao')
    Email = request.args.get('Email')

    # Formatação do Cep
    CEP = FormatarDocumentos.FomartDocumets.Format_Cep(request.args.get('CEP'))
    Cidade = request.args.get('Cidade')
    Rua = request.args.get('Rua')
    NumeroCasa = request.args.get('NumeroCasa')
    bairro = request.args.get('Bairro')

    barco = request.args.get('barco')

    """ Inicio do código para criar arquivo PDF"""
    html_renderizado = render_template('Procuracao.html', nome=nome, cpf=cpf, DataNascimento=DataNascimento,
                                       RG=RG, EstadoCivil=EstadoCivil, OrgaoEmissor=OrgaoEmissor,
                                       DataEmissao=DataEmissao,
                                       Telefone=Telefone, Nacionalidade=Nacionalidade, LocalNascimento=LocalNascimento,
                                       Profissao=Profissao, Email=Email,
                                       CEP=CEP, Cidade=Cidade, Rua=Rua, NumeroCasa=NumeroCasa, bairro=bairro,
                                       barco=barco)

    filePath = os.path.abspath("templates/Procuracao.html")

    fileUrl = pathlib.Path(filePath).as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        pasta = os.path.join(os.getcwd(), 'ArquivosPDF\\')

        page.goto('http://127.0.0.1:8000/GerarPDF')

        page.emulate_media(media='print')

        page.set_content(html_renderizado)

        page.pdf(path=f"{pasta}Procuracao_{nome}.pdf")

        # Envio dos das informações do arquivo para o bando de dados

        id_File = LinksGeneration.Token.query.filter_by(id=id).first()

        fileName = f'Procuracao_{nome}.pdf'  # Salva o nome do arquivo no banco de dados

        DateFilled = date.today()  # Salva a data que o arquivo for preenchido

        Files.Files.query.filter_by(id=id).update(
            {'Name': fileName, 'User': nome, 'Date': DateFilled})
        Config.db.session.commit()

        # Fechamento do navegador para finalizar a criação do arquivo
        browser.close()

    """ Inicia o envio de email """
    Get_user_Email = session.get('user_email')
    Get_Access_Token = session.get('access_token')

    Access_Token = Get_Access_Token
    Destinatario = Get_user_Email
    EnviarEmail.EnviarEmail.email(Email, Destinatario, nome,
                                  Access_Token)
    return redirect('/DashBoard')
