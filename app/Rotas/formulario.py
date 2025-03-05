from app import app, Config
from flask import render_template, request, redirect, url_for
import os
from itsdangerous import SignatureExpired, BadSignature
from Models import LinksGeneration


@app.route('/Form/<id>/<token>/<Files_id>', methods=['GET', 'POST'])
def procuracao(id, token, Files_id):
    action = request.form.get('action')

    NomeCompleto = request.form.get('NomeCompleto')
    CPFCompleto = request.form.get('CPFCompleto')
    DataDeNascimento = request.form.get('DataDeNascimento')
    RgCompleto = request.form.get('RgCompleto')
    EstadoCivil = request.form.get('EstadoCivil')
    OrgaoEmissor = request.form.get('Emissor')
    DataDeEmicaoRG = request.form.get('DataDeEmicaoRG')

    telefone = request.form.get('telefone')
    Nacionalidade = request.form.get('Nacionalidade')
    LocalDeNascimento = request.form.get('LocalDeNascimento')
    Profissao = request.form.get('Profissao')
    Email = request.form.get('EmailCompleto')

    Rua = request.form.get('Rua')
    CEP = request.form.get('CEPCompleto')
    NumeroCasa = request.form.get('NumeroCasa')
    Bairro = request.form.get('Bairro')
    Cidade = request.form.get('Cidade')

    barco = request.form.get('barco')

    try:
        id_token = LinksGeneration.Token.query.filter_by(id=id, token=token, Files_id=Files_id).first()

        if not id_token:
            return 'Link não encotrado', 400

        if id_token.is_used:
            Title = 'Obrigado por preencher nosso formulário, :)'
            Message = 'Entraremos em contato em breve para completar seu chamado!'
            isform = True
            return render_template('Erro.html', Title=Title, Message=Message, isform=isform)

        if request.method == 'POST':
            id_token.is_used = True
            Config.db.session.commit()
            pasta = os.path.join(os.getcwd(), 'ArquivosPDF\\')
            if action == 'Gerar':
                return redirect(url_for('GerarPDF', id=id_token.Files_id, NomeCompleto=NomeCompleto,
                                        CPFCompleto=CPFCompleto,
                                        DataDeNascimento=DataDeNascimento,

                                        RgCompleto=RgCompleto,
                                        EstadoCivil=EstadoCivil,
                                        OrgaoEmissor=OrgaoEmissor,
                                        DataDeEmicaoRG=DataDeEmicaoRG,

                                        telefone=telefone,
                                        Nacionalidade=Nacionalidade,
                                        LocalDeNascimento=LocalDeNascimento,
                                        Profissao=Profissao,
                                        Email=Email,

                                        Rua=Rua,
                                        CEP=CEP,
                                        NumeroCasa=NumeroCasa,
                                        Bairro=Bairro,
                                        Cidade=Cidade,

                                        barco=barco))
            return 'Formulário preenchido', 200

    except SignatureExpired:
        return 'Link Expirou', 403
    except BadSignature:
        return 'Link Enviado', 403

    return render_template('test.html',
                           id_token=id_token,

                           NomeCompleto=NomeCompleto,
                           CPFCompleto=CPFCompleto,
                           DataDeNascimento=DataDeNascimento,

                           RgCompleto=RgCompleto,
                           EstadoCivil=EstadoCivil,
                           OrgaoEmissor=OrgaoEmissor,
                           DataDeEmicaoRG=DataDeEmicaoRG,

                           telefone=telefone,
                           Nacionalidade=Nacionalidade,
                           LocalDeNascimento=LocalDeNascimento,
                           Profissao=Profissao,
                           Email=Email,

                           Rua=Rua,
                           CEP=CEP,
                           NumeroCasa=NumeroCasa,
                           Bairro=Bairro,
                           Cidade=Cidade,

                           barco=barco
                           )
