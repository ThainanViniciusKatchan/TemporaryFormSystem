class ListaDados:
    def Links(Models) -> "Informações do banco de dados":  # Função para mostrar todos so clientes
        Links = []
        for Link in Models:
            cliente_dict = {
                'id': Link.id,
                'token': Link.token,
                'Creation_data': Link.Creation_data,
                'is_used': Link.is_used,
            }
            Links.append(cliente_dict)
        return Links
