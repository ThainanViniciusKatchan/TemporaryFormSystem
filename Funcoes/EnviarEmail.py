from os import path, listdir, getcwd
from os.path import isfile
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests


class EnviarEmail:
    @staticmethod
    def email(remetente, destinatario, nome, access_token):
        # passando informações de remetente e destinatário
        msg = MIMEMultipart()
        msg["Subject"] = f"Procuração Particular do(a) Senhor(a) {nome}"
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Replay-To"] = remetente

        # Corpo do e-mail
        corpo_email = f"Segue em anexo os documentos solicitados do(a) Senhor(a) {nome}."
        msg.attach(MIMEText(corpo_email, "plain"))

        # Localizar e abrir o arquivo que será enviado
        caminho = path.join(getcwd(), 'ArquivosPDF\\')
        arquivos = listdir(caminho)

        for file in arquivos:
            caminhoCompleto = path.join(caminho, file)
            if isfile(caminhoCompleto):
                with open(caminhoCompleto, "rb") as f:
                    part = MIMEBase("application", "pdf")
                    part.set_payload(f.read())

            # Codificando os arquivos para serem enviados
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disporsition",
                f'attachment; filename="{file}"')
            part.add_header(
                "content-type",
                "application/pdf", name=file)
            msg.attach(part)

        # Converte a mensagem para o formato da API do Gmail
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode().replace("\n", "")

        # Enviar e-mail via Gmail API
        url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = json.dumps({"raw": raw_message})

        response = requests.post(url, headers=headers, data=data)

        # Retorno de sucesso ou erro ao enviar
        if response.status_code == 200:
            return "E-mail enviado com sucesso!"
        else:
            return f"Erro ao enviar e-mail: {response.text}"
