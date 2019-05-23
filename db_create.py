#!/usr/bin/python3
import pymysql
import os
from data_gen import generate_database

def imprimir_resposta(response, header):
	if (response):
		width_res = max(len(str(word)) for row in response for word in row)
		width_header = max(len(str(word)) for row in header for word in row)
		col_width = max(width_res, width_header) + 2
		
		for row in header:
			print ("".join(str(word).ljust(col_width) for word in row))
		for row in response:
			print("".join(str(word).ljust(col_width) for word in row))
		input("Aperte Enter ao terminar")
	else:
		input("Nenhuma cirurgia. Aperte Enter para retornar")

clear = lambda: os.system('cls')

# Open database connection
db = pymysql.connect("localhost", "jonathas", passwd="EiC9Shei", db="mc536")

cur = db.cursor()

setup_commands = generate_database()

cur.execute("DROP TABLE IF EXISTS realiza_cirurgia;") 
cur.execute("DROP TABLE IF EXISTS cirurgia;") 
cur.execute("DROP TABLE IF EXISTS exame;") 
cur.execute("DROP TABLE IF EXISTS consulta;") 
cur.execute("DROP TABLE IF EXISTS diagnostico;")
cur.execute("DROP TABLE IF EXISTS internacao;")
cur.execute("DROP TABLE IF EXISTS medico;")
cur.execute("DROP TABLE IF EXISTS paciente;")
cur.execute("DROP TABLE IF EXISTS enfermeiro;")
cur.execute("DROP TABLE IF EXISTS funcionario;")  
cur.execute("DROP TABLE IF EXISTS sala;") 

for command in setup_commands:
  print(command)
  cur.execute(command)

db.commit()

while (1):
	clear()
	print("Escolha o tipo de usuário:\
		\n\t1 - Médico\
		\n\t2 - Enfermeiro\
		\n\t3 - Paciente\
		\nPara sair escolha 0")
	entry = input("Escolha um número: ")

	if (entry == '0'):
		break

	# Caso seja médico
	elif (entry == '1'):
		medId = input("Digite seu ID: ")

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Consultar cirurgias a fazer\
				\n\t2 - Consultar pacientes\
				\n\t3 - Consultar exames de um paciente\
				\n\t4 - Consultar diagnósticos de um paciente\
				\n\t0 - Para retornar")
			entry = input("Escolha um número: ")

			if (entry == '0'):
				break

			# Caso escolha cirurgia
			elif (entry == '1'):
				cur.execute("SELECT paciente.nome, idsala, tipo, data, horario FROM funcionario\
					INNER JOIN realiza_cirurgia ON realiza_cirurgia.ID=funcionario.ID\
					INNER JOIN cirurgia ON cirurgia.ncirurgia=realiza_cirurgia.ncirurgia\
					INNER JOIN paciente ON cirurgia.cpf=paciente.cpf\
					WHERE funcionario.ID="+medId+";")

				header = [["Paciente", "Sala", "Tipo", "Data", "Horário"]]
				imprimir_resposta(cur.fetchall(), header)
			
			#Caso escolha consultar pacientes
			elif (entry == '2'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Consultar paciente por nome\
					\n\t2 - Consultar paciente por CPF\
					\n\tPara retornar escolha 0")
				entry = input("Escolha um número: ")

				if (entry == '0'):
					continue

				# Caso escolha consultar por nome
				elif (entry == '1'):
					nomePaciente = input("Digite o nome desejado: ")
					cur.execute("SELECT nome, cpf, datanascimento, genero, tiposang\
						FROM Paciente WHERE Nome LIKE'"+nomePaciente+"%';")
					
					header = [["Nome", "CPF", "Data Nascimento", "Gênero", "Tipo Sanguíneo"]]
					imprimir_resposta(cur.fetchall(), header)

				# Caso escolha consultar por CPF
				elif (entry == '2'):
					cpfPaciente = input("Digite o CPF do paciente: ")
					while (len(cpfPaciente) != 11):
						cpfPaciente = input("Tamanho invalido. Tente Novamente: ")
					cur.execute("SELECT nome, cpf, datanascimento, genero, tiposang\
						FROM Paciente WHERE CPF='"+cpfPaciente+"';")

					header = [["Nome", "CPF", "Data Nascimento", "Gênero", "Tipo Sanguíneo"]]
					imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar exame de paciente
			elif (entry == '3'):
				cpfPaciente = input("Digite o CPF do paciente: ")
				cur.execute("SELECT Nome, Tipo, Data, Horario, Local FROM Paciente\
					INNER JOIN Exame ON Exame.CPF=Paciente.CPF\
					WHERE Paciente.CPF='"+cpfPaciente+"';")

				header = [["Nome", "Tipo", "Data", "Horário", "Sala"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar diagnósticos de paciente
			elif (entry == '4'):
				cpfPaciente = input("Digite o CPF do paciente: ")
				cur.execute("SELECT Nome, Patologia, SIntomas FROM Paciente\
					INNER JOIN Diagnostico ON Diagnostico.CPF=Paciente.CPF\
					WHERE Paciente.CPF='"+cpfPaciente+"';")

				header = [["Nome", "Patologia", "Sintomas"]]
				imprimir_resposta(cur.fetchall(), header)

	# Caso seja enfermeiro
	elif (entry == '2'):
		enfId = input("Digite seu ID: ")

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Consultar cirurgias\
				\n\t2 - Consultar paciente por nome\
				\n\t3 - Consultar internações\
				\n\tPara sair escolha 0")
			entry = input("Escolha um número: ")

			if (entry == '0'):
				break

			# Caso escolha cirurgias	
			elif (entry == '1'):
				cur.execute("SELECT paciente.nome, idsala, tipo, data, horario  FROM funcionario\
					INNER JOIN Realiza_cirurgia ON funcionario.ID=Realiza_cirurgia.ID\
					INNER JOIN cirurgia ON cirurgia.ncirurgia=realiza_cirurgia.ncirurgia\
					INNER JOIN paciente ON cirurgia.CPF=paciente.CPF\
					WHERE funcionario.Id='"+enfId+"';")
				
				header = [["Paciente", "Sala", "Tipo", "Data", "Horário"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar paciente por nome
			elif (entry == '2'):
				nomePaciente = input("Digite o nome desejado: ")
				cur.execute("SELECT nome, cpf, datanascimento, genero, tiposang\
					FROM Paciente WHERE Nome='"+nomePaciente+"';")
				
				header = [["Nome", "CPF", "Data Nascimento", "Gênero", "Tipo Sanguíneo"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar internação de paciente
			elif (entry == '3'):
				cpfPaciente = input("Digite o CPF do paciente: ")
				cur.execute("SELECT nome, idsala, data_entrada, data_alta FROM Paciente\
					INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
					WHERE Paciente.CPF='"+cpfPaciente+"';")
				
				header = [["Paciente", "Sala", "Data de entrada", "Data de alta"]]
				imprimir_resposta(cur.fetchall(), header)

	# Caso seja paciente
	elif (entry == '3'):
		cpfPaciente = input("Digite seu CPF: ")

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Consultar cirurgias a fazer\
				\n\t2 - Consultar internação\
				\n\t3 - Constular exames\
				\n\t4 - Consultar diagnósticos\
				\n\tPara sair escolha 0")
			entry = input("Escolha um número: ")

			if (entry == '0'):
				break

			# Caso escolha cirurgia 
			elif (entry == '1'):
				cur.execute("SELECT idsala, tipo, data, horario FROM paciente\
					INNER JOIN cirurgia ON paciente.CPF = cirurgia.CPF\
					WHERE paciente.CPF='"+cpfPaciente+"';")
				
				header = [["Sala", "Tipo", "Data", "Horário"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha internação
			elif (entry == '2'):
				cur.execute("SELECT idsala, data_entrada, data_alta FROM paciente\
					INNER JOIN internacao ON paciente.CPF=internacao.CPF\
					WHERE paciente.CPF='"+cpfPaciente+"';")
				
				header = [["Sala", "Data de entrada", "Data de alta"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha exame
			elif (entry == '3'):
				cur.execute("SELECT tipo, data, local FROM paciente\
					INNER JOIN exame ON paciente.CPF=exame.CPF\
					WHERE paciente.CPF='"+cpfPaciente+"';")

				header=[["Tipo", "Data", "Local"]]
				imprimir_resposta(cur.fetchall(), header)
				

			# Caso escolha diagnóstico
			elif (entry == '4'):
				cur.execute("SELECT funcionario.nome, patologia, sintomas FROM paciente\
					INNER JOIN diagnostico ON paciente.CPF=diagnostico.CPF\
					INNER JOIN funcionario ON funcionario.id=diagnostico.idmedico\
					WHERE paciente.CPF='"+cpfPaciente+"';")
			
				header=[["Médico responsável", "Diagnóstico", "Sintomas"]]
				imprimir_resposta(cur.fetchall(), header)

	else:
		print("Entrada não válida\n")

db.close()