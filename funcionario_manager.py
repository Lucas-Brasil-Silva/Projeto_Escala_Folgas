import json

class Funcionario:
    """
    Essa classe Funcionario permite a adição, remoção e visualização de funcionários em um arquivo JSON. 
    Os funcionários são armazenados em um arquivo chamado 'funcionarios.json'.
    A classe Funcionario oferece métodos estáticos para realizar essas operações, garantindo que os dados sejam mantidos e atualizados no arquivo.
    """

    arquivo_nome = "arquivos/funcionarios.json"

    @classmethod
    def adicionar(cls, funcionario):
        try:
            with open(cls.arquivo_nome, "r", encoding="UTF-8") as arquivo:
                dados_existentes = json.load(arquivo)
        except FileNotFoundError:
            dados_existentes = {"funcionarios": []}

        dados_existentes["funcionarios"].append(funcionario)
        with open(cls.arquivo_nome, "w", encoding="UTF-8") as arquivo:
            json.dump(dados_existentes, arquivo, indent=4)

    @classmethod
    def remover(cls, funcionario):
        with open(cls.arquivo_nome, "r", encoding="UTF-8") as arquivo:
            dados_existentes = json.load(arquivo)

        dados_existentes["funcionarios"].remove(funcionario)
        with open(cls.arquivo_nome, "w", encoding="UTF-8") as arquivo:
            json.dump(dados_existentes, arquivo, indent=4)

    @classmethod
    def visualizar(cls):
        try:
            with open(cls.arquivo_nome, "r", encoding="UTF-8") as arquivo:
                dados = json.load(arquivo)
            return dados["funcionarios"]
        except FileNotFoundError:
            return []