import datetime
from app import app, Config
from flask import url_for, session
from Models import LinksGeneration, Files


def gerar_token_link() -> str:
    Creation_data = datetime.datetime.now()
    token_link = Config.serializer.dumps({'expires_at': str(Creation_data)})

    # Criar uma coluna vazia na tabela de arquivo que será preenchida quando o arquivo for gerado
    NovoidArquivo = Files.Files(Name='None', Date=datetime.datetime.utcnow(), User='None')
    Config.db.session.add(NovoidArquivo)
    Config.db.session.commit()

    User_id = session.get('User_id')  # Resgata da sessão o id do usuário logado

    # Enviando para o banco de dados o token, data de expiração e se o link já foi usado
    novo_link = LinksGeneration.Token(token=token_link, Creation_data=Creation_data, is_used=False,
                                      Files_id=NovoidArquivo.id, User_id=User_id)
    Config.db.session.add(novo_link)
    Config.db.session.commit()

    # Gera a URL completa para o formulário
    link = url_for('procuracao', id=novo_link.id, token=token_link, Files_id=NovoidArquivo.id, _external=True)
    return link, Creation_data


# Exemplo de uso:
if __name__ == "__main__":
    with app.app_context():
        link, Creation_data = gerar_token_link()
        print(f"Link gerado: {link}")
        print(f"Expira em: {Creation_data}")
