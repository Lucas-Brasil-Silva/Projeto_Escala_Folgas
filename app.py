"""
Este programa permite que os usuários gerem uma escala de trabalho com base em dados de funcionários e dias do mês. Ele fornece uma interface gráfica simples para adicionar, remover e visualizar funcionários, além de gerar uma escala de trabalho em um arquivo Excel.

Funções Principais:
- pagina_inicial(): Cria a interface gráfica da página inicial.
- mostrar_instrucoes(): Mostra as instruções em uma janela pop-up.
- adicionar_funcionario(): Adiciona um funcionário à lista.
- remover_funcionario(): Remove um funcionário da lista.
- visualizar_funcionarios(): Exibe a lista de funcionários registrados.
- gerar_escala(): Gera uma escala de trabalho com base nos dados fornecidos.

Notas:
- Certifique-se de que os módulos funcionario_manager, gerador_escala_trabalho e planilha_gerador estejam disponíveis no mesmo diretório do programa.
- O programa pode ser personalizado para atender às necessidades específicas de escalas de trabalho e funcionários.
"""

import PySimpleGUI as pg
from funcionario_manager import Funcionario
from gerador_escala_trabalho import dias_mes, dados_escala
from planilha_gerador import Planilha
from datetime import datetime

pg.theme("Reddit")

def pagina_inicial():
    meses = [str(i) for i in range(1, 13)]
    dias = [str(i) for i in range(1, 32)]

    layout = [
        [
            pg.Text("Altere o mês, dia ou ambos para valores que o interessam:"),
            pg.Text("", size=(2, 1)),
            pg.Button(
                image_filename="imagens/livro.PNG", image_subsample=4, pad=(0), key="instrucoes"
            ),
        ],
        [
            pg.Text("Mês: "),
            pg.Combo(
                values=meses,
                default_value=str(datetime.now().month),
                size=(3, 12),
                key="mes",
            ),
            pg.Text("Dia inicial: "),
            pg.Combo(values=dias, default_value="1", size=(3, 10), key="dia"),
        ],
        [pg.Text("Adicione, remova ou visualize funcionários registrados.")],
        [pg.Input(key="funcionario")],
        [
            pg.Button(button_text="Adicionar", button_color="Green", key="adicionar"),
            pg.Button(button_text="Remover", button_color="Red", key="remover"),
            pg.Button(
                button_text="Visualizar",
                key="visualizar",
            ),
        ],
        [
            pg.Text("*", text_color="Red", font=("", 14), pad=(2)),
            pg.Text(
                'Informe o nome e onde o arquivo será salvo, clicando em "Save As...',
                pad=(0, 0),
            ),
        ],
        [pg.Input(key="arquivo"), pg.FileSaveAs(file_types=((".xlsx", "*.xlsx"),))],
        [pg.Button(button_text="Gerar Escala", key="gerar")],
    ]

    return pg.Window(title="Pagina Inicial", layout=layout, finalize=True)

def mostrar_instrucoes():
    with open("arquivos/instrucoes.txt", encoding="UTF-8") as arquivo:
        texto = arquivo.read()
    pg.popup_scrolled(texto, title="Instruções", font=("Arial", 13), size=(55, 10))

def adicionar_funcionario(window, nome):
    if nome:
        Funcionario.adicionar(nome)
        window["funcionario"].update("")
        pg.popup_ok(
            "Funcionário adicionado com sucesso!",
            title="Adicinar funcionário",
        )
    else:
        pg.popup("Por favor, Digite um nome!", title="Funcinário")

def remover_funcionario(window, nome):
    if nome:
        try:
            Funcionario.remover(nome)
            window["funcionario"].update("")
            pg.popup_ok(
                "Funcionario removido com sucesso!", title="Removendo funcionario"
            )
        except ValueError:
            pg.popup_error("Funcionário não registrado!", title="Erro")
    else:
        pg.popup("Por favor, Digite um nome!", title="Funcinario")

def visualizar_funcionarios():
    funcionarios = " - ".join(Funcionario.visualizar())
    if funcionarios:
        pg.popup_scrolled(
            funcionarios,
            title="Funcinários Registrados",
            font=("Arial", 14),
            size=(45, 10),
        )
    else:
        pg.popup_ok("Sem funcionários registrados!", title="Aviso")

def gerar_escala(window, values):
    dia = int(values["dia"]) if values["dia"] else 0
    mes = int(values["mes"]) if values["mes"] else None
    lista_dias = dias_mes(dia, mes)
    lista_funcionarios = Funcionario.visualizar()
    caminho = values["arquivo"]
    if caminho:
        folgas, homeoffice, plantoes = dados_escala(lista_dias, lista_funcionarios)
        planilha_ = Planilha(caminho, mes)
        planilha_.gerar_escala(folgas, homeoffice, plantoes)
        window["arquivo"].update("")
        window["dia"].update(1)
        mes_ = datetime.now().month
        window["mes"].update(mes_)
    else:
        pg.popup(
            "Por favor, informa o nome e onde o arquivo será gerado!", title="Aviso"
        )

def main():
    mostrar_instrucoes()
    pagina_inicial_ = pagina_inicial()

    while True:
        window, event, values = pg.read_all_windows()
        if event == pg.WIN_CLOSED:
            break
        elif window == pagina_inicial_:
            if event == "instrucoes":
                mostrar_instrucoes()

            elif event == "adicionar":
                adicionar_funcionario(pagina_inicial_, values["funcionario"])

            elif event == "remover":
                remover_funcionario(pagina_inicial_, values["funcionario"])

            elif event == "visualizar":
                visualizar_funcionarios()

            elif event == "gerar":
                gerar_escala(pagina_inicial_, values)

if __name__ == "__main__":
    main()