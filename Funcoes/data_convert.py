from datetime import datetime


class DataConverter:
    def formatar(data) -> str == 'Data formatada para o arquivo pdf':
        data_corrigida = data.replace('-', '/')
        formatar_data = datetime.strptime(data_corrigida, '%Y/%m/%d')
        data_formatada = formatar_data.strftime('%d/%m/%Y')
        return data_formatada
