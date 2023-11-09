# Importações necessárias
from calendar import monthrange, day_name, weekday
from datetime import datetime
import random

def dias_mes(dia=0,mes=None):
    """
    Descrição: Gera uma lista de dias do mês com seus respectivos nomes dos dias da semana.
    Parâmetros:
       - dia (int): O dia inicial (padrão é 0 para o primeiro dia do mês).
       - mes (int): O mês desejado (padrão é None para o mês atual).
    Retorna: Uma lista de tuplas contendo o nome do dia da semana e o número do dia.
    """

    mes_ = mes if mes else datetime.now().month
    ano = datetime.now().year
    total_dias = monthrange(ano,mes_)[1]
    return [(day_name[weekday(ano,mes_,dia_)],dia_) for dia_ in range(1,total_dias+1) if dia <= dia_]

def gerar_folgas(dias,funcionarios):
    """ 
    Descrição: Gera uma lista de folgas para os funcionários com base nos dias da semana.
    Parâmetros:
    - dias (list): Lista de dias gerada pela função dias_mes.
    - funcionarios (list): Lista de funcionários disponíveis.
    Retorna: Uma lista de folgas atribuídas a funcionários.
    """

    random.shuffle(funcionarios)
    sabados = [[nome,dia] for nome, dia in dias if nome == 'Saturday']
    folgas = [[funcionario, dia[0],dia[1]] for funcionario, dia in zip(funcionarios, sabados * len(funcionarios))]
    return folgas

def dividir_semanas(dias):
    """ 
    Descrição: Divide os dias em semanas, excluindo os domingos.
    Parâmetros:
      - dias (list): Lista de dias gerada pela função dias_mes.
    Retorna: Uma lista de semanas de trabalho.
    """

    semanas = []
    dados = []
    for nome,dia in dias:
        if nome != 'Sunday':
            dados.append([nome,dia])
        else:
            if len(dados) != 0:
                semanas.append(dados)
            dados = []
    if len(dados) != 0:
        semanas.append(dados)
    return semanas

def criar_homebruto(semanas,funcionarios):
    """ 
    Descrição: Cria a programação bruta de home office, equilibrando a atribuição de dias.
    Parâmetros:
      - semanas (list): Lista de semanas de trabalho.
      - funcionarios (list): Lista de funcionários disponíveis.
    Retorna: Uma lista de programação bruta de home office.
    """

    homebruto = []
    for semana in semanas:
        random.shuffle(funcionarios)
        dados = []
        alterar = []
        if len(funcionarios) >= len(semana):
            for i in  range(len(funcionarios)):
                dia = semana[i % len(semana)]
                if dia[0] in 'Saturday':
                    alterar.append([funcionarios[i],dia])
                dados.append([funcionarios[i],dia])
                try:
                    for dado in alterar:
                        dados.remove(dado)
                        dados.append(dado)
                except Exception:
                    pass
            homebruto.append(dados)
        else:
            for id,dia in enumerate(semana):
                try:
                    dados.append([funcionarios[id],dia])
                except IndexError:
                    dados.append(['Vago',dia])
            homebruto.append(dados)
    return homebruto

def ajustar_homebruto(homebruto,folgas):
    """
    Descrição: Ajusta a programação bruta para evitar conflitos com as folgas dos funcionários.
    Parâmetros:
      - homebruto (list): Programação bruta de home office.
      - folgas (list): Lista de folgas atribuídas aos funcionários.
    """

    folgando = None
    for semana in homebruto:
        for id,dia in enumerate(semana):
            if dia[1][0] == 'Saturday':
                folgando = [dado[0] for dado in folgas if dado[2] == dia[1][1]]
                if dia[0] in folgando:
                    while True:
                        proximo_dia = semana[random.randint(0,id)]
                        if proximo_dia[1][0] != 'Saturday':
                            alterar = proximo_dia.copy()
                            break
                    alterar[0] = dia[0]
                    semana.insert(0,alterar)
                    dia[0] = 'Vago'
            
            elif folgando:
                if dia[0] in folgando:
                    dia[0] = 'Vago'

def gerar_homeoffice(homebruto):
    """ 
    Descrição: Gera a programação de home office com base na programação bruta.
    Parâmetros:
      - homebruto (list): Programação bruta de home office.
    Retorna: Uma programação de home office equilibrada.
    """

    homeoffice = [[dado[0],dado[1][1]] for semana in homebruto for dado in semana if dado[0] != 'Vago']
    return homeoffice

def ajustar_homesabado(folgas,homeoffice):
    """ 
    Descrição: Ajusta a programação de home office para evitar conflitos aos sábados.
    Parâmetros:
      - folgas (list): Lista de folgas atribuídas aos funcionários.
      - homeoffice (list): Programação de home office.
    """

    for dado in folgas:
        dado.remove('Saturday')

    sabados_ = sorted(set([dado[1] for dado in folgas]))
    homesabado = [home for dia in sabados_ for home in homeoffice if dia == home[1]]
    for i in range(1,len(sabados_)+1):
        folga_passada = [dado for dado in folgas if dado[1] == sabados_[i-1]]
        home_dia = [dado for dado in homesabado if dado[1] == sabados_[i]] if i < len(sabados_) else [dado for dado in homesabado if dado[1] == sabados_[i-1]]
        for home in home_dia:
            if any(home[0] in dado for dado in folga_passada):
                homeoffice.remove(home)

def gerar_plantoes(dias, homeoffice, folgas):
    """ 
    Descrição: Gera uma lista de plantões com base na programação de home office e folgas.
    Parâmetros:
      - dias (list): Lista de dias gerada pela função dias_mes.
      - homeoffice (list): Programação de home office.
      - folgas (list): Lista de folgas atribuídas aos funcionários.
    Retorna: Uma lista de plantões atribuídos.
    """

    plantoes = []

    sabados_ = sorted(set([dado[1] for dado in folgas]))
    for dia in sabados_:
        folga_dia = [folga for folga in folgas if dia == folga[1]]
        random.shuffle(folga_dia)
        plantoes.append([random.choice(folga_dia),'P-Plantão'])
    
    for dia in dias:
        home = [home for home in homeoffice if home[1] == dia[1]]
        random.shuffle(home)
        if len(home) != 0:
            dado_ = random.choice(home)
            plantoes.append([dado_,'H-Plantão'])
            homeoffice.remove(dado_)  
    
    return plantoes

def dados_escala(dias,funcionarios):
    """ 
    Descrição: Função principal que gera a programação completa da escala de trabalho.
    Parâmetros:
      - dias (list): Lista de dias gerada pela função dias_mes.
      - funcionarios (list): Lista de funcionários disponíveis.
    Retorna: Três listas contendo as folgas, a programação de home office e os plantões atribuídos.
    """

    folgas = gerar_folgas(dias,funcionarios)
    semanas = dividir_semanas(dias)
    homebruto = criar_homebruto(semanas,funcionarios)
    ajustar_homebruto(homebruto,folgas)
    homeoffice = gerar_homeoffice(homebruto)
    ajustar_homesabado(folgas,homeoffice)
    plantoes = gerar_plantoes(dias,homeoffice,folgas)

    return folgas,homeoffice,plantoes