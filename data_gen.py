# -*- coding: utf-8 -*-
from random import randint, choice, randrange
from itertools import product

### Funcoes auxiliares
def sortear(lista):
    return lista[randint(0,len(lista)-1)]

def gerar_cpf():
    def calcula_digito(digs):
       s = 0
       qtd = len(digs)
       for i in range(qtd):
          s += n[i] * (1+qtd-i)
       res = 11 - s % 11
       if res >= 10: return 0
       return res
    n = [randrange(10) for i in range(9)]
    n.append(calcula_digito(n))
    n.append(calcula_digito(n))
    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)

def gerar_cpf_unico(lista):
    cpf = gerar_cpf()
    while cpf in lista:
        cpf = gerar_cpf()
    return cpf

def gerar_nome_novo(listas_formacao, lista_nomes_existentes):
    nome = []
    for lista in listas_formacao:
        nome.append(sortear(lista))
    while ' '.join(nome) in lista_nomes_existentes:
        nome = []
        for lista in listas_formacao:
            nome.append(sortear(lista))
    return ' '.join(nome)

# formato 10 digitos e estado
def gerar_crm(estados):
    num = randint(1000000000,9999999999)
    estado = sortear(estados)
    return "%010d%s" % (num,estado)

# formato YYYY-MM-DD
def gerar_data(ano_inicial, ano_final):
    ano = randint(ano_inicial,ano_final)
    mes = randint(1,12)
    if(mes == 2):
      dia = randint(1,28)
    else:
      dia = randint(1,30)
    return "%04d-%02d-%02d" % (ano,mes,dia)

# formato HH:MM
def gerar_horario(hora_inicial, hora_final):
    hora = randint(hora_inicial,hora_final)
    minuto = randint(0,59)
    segundo = randint(0,59)
    return "%02d:%02d:%02d" % (hora,minuto, segundo)

### Geradores
PEOPLE_NAMES_H = ['Diogo','Felipe','Matheus','Vinicius','Leonardo','Otávio','Rodrigo','Kauê','Samuel','Tiago'] # homens
PEOPLE_NAMES_M = ['Ana','Sara','Brenda','Isabelle','Beatriz','Emilly','Lara','Maria','Clara','Fernanda'] # mulheres
PEOPLE_SURNAMES = ['Barros','Martins','Araujo','Carvalho','Cardoso','Almeida','Fernandes','Ribeiro','Rocha','Ferreira']  # sobrenomes
GENDER = ['H','M']
BLOOD_TYPES = ['A+','A-','B+','B-','AB+','AB-','O+','O-']
ESTADOS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ',
'RN','RS','RO','RR','SC','SP','SE','TO']
ESPECIALIDADES = ['Anestesia','Imunologia','Cardiologia','Pediatria','Cirurgia Geral','Gastroentorologia','Geriatria',
'Ginecologia','Infectologia','Neurologia','Oftalmologia','Ortopedia','Otorrinolaringologia','Psiquiatria','Urologia']
TIPOS_SALAS = ['Cirurgia','Quarto','UTI','Consultorio','Exame']
TIPOS_EXAMES = ['Raio X','Mamografia','Desintometria óssea','Ressonância Magnética','Tomografia Computadorizada'
,'Ultra-sonografia','Endoscopia','Hemograma','Urografia','Ecodoppler']
TIPOS_PATOLOGIAS = ['Asma', 'Diabetes', 'AVC', 'Infarte', 'Pneumonia', 'Dengue', 'Gripe', 'Bronquite', 'Micose', 'Intoxicação Alimentar']
TIPOS_SINTOMAS = ['Coceira', 'Febre', 'Coriza', 'Dor de cabeça', 'Dor no corpo', 'Nariz sangrando', 'Hipertensão', 'Garganta inflamada', 'Desidratação']
TIPOS_CIRURGIAS = ['Rinoplastia', 'Ortoplastia', 'Ninfoplastia', 'Mamoplastia', 'Lipoaspiração', 'Biópsia', 'Endoscopia', 'Fimose']

'''
Retorna lista de pacientes = (cpf,nome,data,genero,tiposang)
'''
def gerar_pacientes(quantidade):
    pacientes = []
    cpfs = []
    nomes = []
    datas = []
    generos = []
    tipossang = []

    for _ in range(quantidade):
        cpfs.append(gerar_cpf_unico(cpfs))

        genero = sortear(GENDER)
        generos.append(genero)

        if (genero == 'H'):
            nome = gerar_nome_novo([PEOPLE_NAMES_H,PEOPLE_SURNAMES], nomes)
        else:
            nome = gerar_nome_novo([PEOPLE_NAMES_M,PEOPLE_SURNAMES], nomes)

        nomes.append(nome)
        datas.append(gerar_data(1950,2010))
        tiposang = sortear(BLOOD_TYPES)
        tipossang.append(tiposang)

        pacientes.append((cpfs[-1],nomes[-1],datas[-1],generos[-1],tipossang[-1]))
    return pacientes

'''
Retorna lista de medicos = (id,cpf,nome,crm,especialidade)
'''
def gerar_medicos(id_start,quantidade):
    medicos = []
    ids = []
    cpfs = []
    nomes = []
    crms = []
    especialidades = []

    for i in range(quantidade):

        ids.append(i+id_start)
        cpfs.append(gerar_cpf_unico(cpfs))
        genero = sortear(GENDER)

        if (genero == 'H'):
            nome = gerar_nome_novo([PEOPLE_NAMES_H,PEOPLE_SURNAMES], nomes)
        else:
            nome = gerar_nome_novo([PEOPLE_NAMES_M,PEOPLE_SURNAMES], nomes)

        nomes.append(nome)
        crms.append(gerar_crm(ESTADOS))
        especialidades.append(sortear(ESPECIALIDADES))

        medicos.append((ids[-1],cpfs[-1],nomes[-1],crms[-1],especialidades[-1]))
    return medicos

'''
Retorna lista de enfermeiros = (id,cpf,nome,setor)
'''
def gerar_enfermeiros(id_start,quantidade):
    enfermeiros = []
    ids = []
    cpfs = []
    nomes = []
    setores = []

    for i in range(quantidade):

        ids.append(i+id_start)
        cpfs.append(gerar_cpf_unico(cpfs))
        genero = sortear(GENDER)

        if (genero == 'H'):
            nome = gerar_nome_novo([PEOPLE_NAMES_H,PEOPLE_SURNAMES], nomes)
        else:
            nome = gerar_nome_novo([PEOPLE_NAMES_M,PEOPLE_SURNAMES], nomes)

        nomes.append(nome)
        setores.append(sortear(ESPECIALIDADES))

        enfermeiros.append((ids[-1],cpfs[-1],nomes[-1],setores[-1]))
    return enfermeiros

'''
Retorna lista de salas = (idsala,tipo,capacidade)
'''
def gerar_salas(quantidade):
    salas = []
    ids = []
    tipos = []
    capacidades = []

    for i in range(quantidade):

        ids.append("%03d" % (i+1))
        tipo = sortear(TIPOS_SALAS)
        tipos.append(tipo)

        if (tipo == 'Cirurgia'):
            capacidade = 1
        else:
            capacidade = randint(1,6)

        capacidades.append(capacidade)

        salas.append((ids[-1],tipos[-1],capacidades[-1]))
    return salas

'''
Retorna lista de exames = (nexame,cpf,tipo,data,horario,local)
'''
def gerar_exames(nexame_start,cpfs_exist,locais_exist,ano_inicio,ano_final,quantidade):
    exames = []
    nexames = []
    cpfs = []
    tipos = []
    datas = []
    horarios = []
    locais = []

    for i in range(quantidade):

        nexames.append("%03d" % (i+nexame_start))
        cpfs.append(sortear(cpfs_exist))

        sala = sortear(locais_exist)
        (idsala,tipo_sala,_) = sala
        while (tipo_sala != 'Exame'):
            sala = sortear(locais_exist)
            (idsala,tipo_sala,_) = sala
        locais.append(idsala)

        tipos.append(sortear(TIPOS_EXAMES))
        datas.append(gerar_data(ano_inicio,ano_final))
        horarios.append(gerar_horario(6,19))

        exames.append((nexames[-1],cpfs[-1],tipos[-1],datas[-1],horarios[-1],locais[-1]))
    return exames

'''
Retorna lista de diagnosticos = (ndiag,cpf,idmedico,patologia,sintomas)
'''
def gerar_diagnosticos(ndiag_start,ids_exist,cpfs_exist,quantidade):
    diagnosticos = []
    ndiags = []
    cpfs = []
    ids = []
    patologias = []
    sintomas = []

    for i in range(quantidade):

        ndiags.append(i+ndiag_start)

        cpfs.append(sortear(cpfs_exist))
        ids.append(sortear(ids_exist))
        patologias.append(sortear(TIPOS_PATOLOGIAS))
        sintomas.append(sortear(TIPOS_SINTOMAS))

        diagnosticos.append((ndiags[-1],cpfs[-1],ids[-1],patologias[-1],sintomas[-1]))
    return diagnosticos

'''
Retorna lista de cirurgias = (ncirurgia,idsala,cpf,tipo,data,horario)
'''
def gerar_cirurgias(n_start,locais_exist,cpfs_exist,ano_inicio,ano_final,quantidade):
    cirurgias = []
    ncirurgias = []
    idsalas = []
    cpfs = []
    tipos = []
    datas = []
    horarios = []
    locais = []

    for i in range(quantidade):

        ncirurgias.append(i+n_start)

        sala = sortear(locais_exist)
        (idsala,tipo_sala,_) = sala
        while (tipo_sala != 'Cirurgia'):
            sala = sortear(locais_exist)
            (idsala,tipo_sala,_) = sala
        locais.append(idsala)

        cpfs.append(sortear(cpfs_exist))
        tipos.append(sortear(TIPOS_CIRURGIAS))

        datas.append(gerar_data(ano_inicio,ano_final))
        horarios.append(gerar_horario(6,19))

        cirurgias.append((ncirurgias[-1],locais[-1],cpfs[-1],tipos[-1],datas[-1],horarios[-1]))
    return cirurgias

'''
Retorna lista de internacoes = (idsala,cpf,data_entrada,data_alta)
'''

def gerarDataCoerente(dataAntes, ano_inicio, ano_final):
    anoA = dataAntes[0:4]
    mesA = dataAntes[5:7]
    diaA = dataAntes[8:10]
    dataDepois = gerar_data(ano_inicio, ano_final)
    anoD = dataDepois[0:4]
    mesD = dataDepois[5:7]
    diaD = dataDepois[8:10]
    while(not(anoA<=anoD and mesA<=mesD and diaA<=diaD)):
        dataDepois = gerar_data(ano_inicio, ano_final)
        anoD = dataDepois[0:4]
        mesD = dataDepois[5:7]
        diaD = dataDepois[8:10]
    return dataDepois


def gerar_internacoes(locais_exist,cpfs_exist,ano_inicio,ano_final,quantidade):
    internacoes = []
    idsalas = []
    cpfs = []
    datas_entrada = []
    datas_saida = []
    locais = []

    for _ in range(quantidade):

        cpfs.append(sortear(cpfs_exist))

        sala = sortear(locais_exist)
        (idsala,tipo_sala,_) = sala
        while (tipo_sala != 'UTI' and tipo_sala != 'Quarto'):
            sala = sortear(locais_exist)
            (idsala,tipo_sala,_) = sala
        locais.append(idsala)

        #data entrada tem que ser menor que saida
        dataAntes = gerar_data(ano_inicio,ano_final)
        dataDepois = gerarDataCoerente(dataAntes, ano_inicio, ano_final)

        datas_entrada.append(dataAntes)
        datas_saida.append(dataDepois)

        internacoes.append((locais[-1],cpfs[-1],datas_entrada[-1],datas_saida[-1]))
    return internacoes

'''
Retorna lista de consultas = (id,cpf,data)
'''
def gerar_consultas(ids_exist,cpfs_exist,ano_inicio,ano_final,quantidade):
    consultas = []
    ids = []
    cpfs = []
    datas = []

    for _ in range(quantidade):

        cpfs.append(sortear(cpfs_exist))
        ids.append(sortear(ids_exist))
        datas.append(gerar_data(ano_inicio,ano_final))

        consultas.append((ids[-1],cpfs[-1],datas[-1]))
    return consultas

''' DEF: generate_database(void) : StringArray
    Função a ser chamada quando for necessário inicializar o banco de dados.
    RETORNO: setup_commands[]
            Lista de strings contendo comandos em sql de criação de tabelas
            e inserção de dados.
'''
def generate_database():

    #### GERANDO COMBINAÇÕES DE DADOS ###########
    medicos = gerar_medicos(1, 23)
    med_ids = [i[0] for i in medicos]
    enfermeiros = gerar_enfermeiros(30, 46)
    pacientes = gerar_pacientes(50)
    cpfs = [i[0] for i in pacientes]
    salas = gerar_salas(50)
    idsalas = [i[0] for i in salas]
    print('here')
    exames = gerar_exames(100,cpfs,salas,2010,2018,50)
    print('exams generated')
    diagnosticos = gerar_diagnosticos(5,med_ids,cpfs,50)
    print('diags generated')
    cirurgias = gerar_cirurgias(200,salas,cpfs,2014,2019,25)
    print('cir generated')
    internacoes = gerar_internacoes(salas,cpfs,2010,2018,15)
    print('inter generated')
    consultas = gerar_consultas(med_ids,cpfs,2010,2018,50)
    print('consults generated')

    #### Vetor onde serão inseridos os comandos sql para inicialização do BD
    setup_commands = []

    #### INICIALIZANDO TABELAS ##################
    setup_commands.extend([
    'CREATE TABLE Funcionario (ID int NOT NULL, CPF varchar(11) NOT NULL, Nome varchar(50) NOT NULL, PRIMARY KEY(ID));',
    'CREATE TABLE Medico (ID int NOT NULL, CRM varchar(12) NOT NULL, Especialidade varchar(50), PRIMARY KEY(ID), FOREIGN KEY (ID) REFERENCES Funcionario(ID));',
    'CREATE TABLE Enfermeiro (ID int NOT NULL, Setor varchar(50), PRIMARY KEY(ID), FOREIGN KEY (ID) REFERENCES Funcionario(ID));',
    'CREATE TABLE Paciente (CPF varchar(11) NOT NULL, Nome varchar(50) NOT NULL, DataNascimento DATE NOT NULL, Genero char(1) NOT NULL, TipoSang varchar(3) NOT NULL, PRIMARY KEY(CPF));',
    'CREATE TABLE Exame (NExame int NOT NULL, CPF varchar(11) NOT NULL, Tipo varchar(50) NOT NULL, Data Date, Horario Time(0), Local varchar(50), PRIMARY KEY(NExame), FOREIGN KEY (CPF) REFERENCES Paciente(CPF));',
    'CREATE TABLE Diagnostico (NDiag int NOT NULL, CPF varchar(11) NOT NULL, IDMedico int NOT NULL, Patologia varchar(100), Sintomas varchar(500), PRIMARY KEY(NDiag), FOREIGN KEY (CPF) REFERENCES Paciente(CPF), FOREIGN KEY (IDMedico) REFERENCES Medico(ID));',
    'CREATE TABLE Sala (IDSala int NOT NULL, Tipo varchar(50), Capacidade int, PRIMARY KEY(IDSala));',
    'CREATE TABLE Cirurgia (NCirurgia int NOT NULL, IDSala int NOT NULL, CPF varchar(11) NOT NULL, Tipo varchar(50) NOT NULL, Data Date NOT NULL, Horario Time(0) NOT NULL, PRIMARY KEY(NCirurgia), FOREIGN KEY (IDSala) REFERENCES Sala(IDSala), FOREIGN KEY (CPF) REFERENCES Paciente(CPF));',
    'CREATE TABLE Realiza_cirurgia (NCirurgia int NOT NULL, ID int NOT NULL, FOREIGN KEY (NCirurgia) REFERENCES Cirurgia(NCirurgia), FOREIGN KEY (ID) REFERENCES Funcionario(ID));',
    'CREATE TABLE Internacao (IDSala int NOT NULL, CPF varchar(11) NOT NULL, Data_entrada Date NOT NULL, Data_alta Date, PRIMARY KEY (CPF, Data_entrada), FOREIGN KEY (IDSala) REFERENCES Sala(IDSala), FOREIGN KEY (CPF) REFERENCES Paciente(CPF));',
    'CREATE TABLE Consulta (ID int NOT NULL, CPF varchar(11) NOT NULL, Data Date NOT NULL, PRIMARY KEY (ID,CPF,Data), FOREIGN KEY (ID) REFERENCES Medico(ID), FOREIGN KEY (CPF) REFERENCES Paciente(CPF));'
    ])

    #### POPULANDO BANCO DE DADOS ###############

    # Medico
    for (id,cpf,nome,crm,especialidade) in medicos:
        setup_commands.append("INSERT INTO Funcionario VALUES ("+str(id)+",'"+str(cpf)+"','"+nome+"');")
        setup_commands.append("INSERT INTO Medico VALUES ("+str(id)+",'"+crm+"','"+especialidade+"');")

    # Enfermeiro
    for (id,cpf,nome,setor) in enfermeiros:
        setup_commands.append("INSERT INTO Funcionario VALUES ("+str(id)+",'"+str(cpf)+"','"+nome+"');")
        setup_commands.append("INSERT INTO Enfermeiro VALUES ("+str(id)+",'"+setor+"');")

    # Paciente
    for (cpf,nome,data,genero,tiposang) in pacientes:
        setup_commands.append("INSERT INTO Paciente VALUES ('"+str(cpf)+"','"+nome+"','"+data+"','"+genero+"','"+tiposang+"');")

    # Sala
    for (idsala,tipo,capacidade) in salas:
        setup_commands.append("INSERT INTO Sala VALUES ("+str(idsala)+",'"+tipo+"',"+str(capacidade)+");")

    # Exame
    for (nexame,cpf,tipo,data,horario,local) in exames:
        setup_commands.append("INSERT INTO Exame VALUES ("+str(nexame)+",'"+str(cpf)+"','"+tipo+"','"+data+"','"+horario+"','"+str(local)+"');")

    # Diagnostico
    for (ndiag,cpf,idmedico,patologia,sintomas) in diagnosticos:
        setup_commands.append("INSERT INTO Diagnostico VALUES ("+str(ndiag)+",'"+str(cpf)+"',"+str(idmedico)+",'"+patologia+"','"+sintomas+"');")

    # Cirurgia
    for (ncirurgia,idsala,cpf,tipo,data,horario) in cirurgias:
        setup_commands.append("INSERT INTO Cirurgia VALUES ("+str(ncirurgia)+","+str(idsala)+",'"+str(cpf)+"','"+tipo+"','"+data+"','"+horario+"');")

        medico1 = choice(medicos)[0]
        setup_commands.append("INSERT INTO Realiza_cirurgia VALUES("+str(ncirurgia)+", "+str(medico1)+");")
        medico2 = choice(medicos)[0]
        while (medico2 == medico1):
          medico2 = choice(medicos)[0] 
        setup_commands.append("INSERT INTO Realiza_cirurgia VALUES("+str(ncirurgia)+", "+str(medico2)+");")

        enf1 = choice(enfermeiros)[0]
        setup_commands.append("INSERT INTO Realiza_cirurgia VALUES("+str(ncirurgia)+", "+str(enf1)+");")
        enf2 = choice(enfermeiros)[0]
        while (enf2 == enf1):
          enf2 = choice(enfermeiros)[0] 
        setup_commands.append("INSERT INTO Realiza_cirurgia VALUES("+str(ncirurgia)+", "+str(enf2)+");")
        enf3 = choice(enfermeiros)[0]
        while (enf3 == enf2 or enf3 == enf1):
            enf3 = choice(enfermeiros)[0]
        setup_commands.append("INSERT INTO Realiza_cirurgia VALUES("+str(ncirurgia)+", "+str(enf3)+");")

    # Internacao
    for (idsala,cpf,data_entrada,data_alta) in internacoes:
        setup_commands.append("INSERT INTO Internacao VALUES ("+str(idsala)+",'"+str(cpf)+"','"+data_entrada+"','"+data_alta+"');")

    # Consulta
    for (id,cpf,data) in consultas:
        setup_commands.append("INSERT INTO Consulta VALUES ("+str(id)+",'"+str(cpf)+"','"+data+"');")

    return setup_commands
