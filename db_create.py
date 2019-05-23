#!/usr/bin/python3
import pymysql
import os
from data_gen import generate_database

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
	print("Escolha o tipo de usuário:\n\t1 - Médico\n\t2 - Enfermeiro\n\t3 - Paciente\nPara sair escolha 0")
	entry = input("Escolha um número: ")

	if (entry == '0'):
		break
	elif (entry == '1'):
		medId = input("Digite seu ID: ")
		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar cirurgias a fazer\n\t2 - Consultar pacientes\n\t3 - Consultar exames de um paciente\n\t 4 - Consultar diagnósticos de um paciente\n\t0 - Para retornar")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break
			elif (entry == '1'):
				cur.execute("SELECT * FROM cirurgia INNER JOIN realiza_cirurgia on realiza_cirurgia.ID="+medId+";")
				response = cur.fetchall()
				for r in response:
					print(str(r))
				input("Aperte Enter ao terminar")
			elif (entry == '2'):
				print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar paciente por nome\n\t2 - Consultar paciente por CPF\n\tPara retornar escolha 0")
				entry = input("Escolha um número: ")
				if (entry == '0'):
					continue
				elif (entry == '1'):
					nomePaciente = input("Digite o nome desejado: ")
					cur.execute("SELECT * FROM Paciente WHERE Nome='"+nomePaciente+"';")
					response = cur.fetchall()
					for r in response:
						print(r)
					input("Aperte Enter ao terminar")
				elif (entry == '2'):
					cpfPaciente = input("Digite o CPF do paciente: ")
					while (len(cpfPaciente) != 11):
						cpfPaciente = input("Tamanho invalido. Tente Novamente: ")
					cur.execute("SELECT * FROM Paciente WHERE CPF='"+cpfPaciente+"';")
					response = cur.fetchall()
					for r in response:
						print(r)
					input("Aperte Enter ao terminar")
			elif (entry == '3'):
				cpfPaciente = input("Digite o CPF do paciente: ")
				cur.execute("SELECT Nome, Tipo, Data, Horario, Local FROM Paciente INNER JOIN Exame ON Exame.CPF=Paciente.CPF WHERE Paciente.CPF='"+cpfPaciente+"';")
				response = cur.fetchall()
				for r in response:
					print(r)
				input("Aperte Enter ao terminar")
	elif (entry == '2'):
		while(1):
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar paciente por nome\n\t2 - Consultar paciente por CPF\nPara sair escolha 0")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break
			elif (entry == '1'):
				entry = input("Escolha um nome: ")
				cur.execute("SELECT * FROM funcionario, medico WHERE Nome='"+entry+"' AND funcionario.ID=medico.ID;")
				print(cur.fetchall())
	elif (entry == '3'):
		while(1):
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar todos os médicos\n\t2 -Consultar médicos por nome\nPara sair escolha 0")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break
			elif (entry == '1'):
				entry = input("Escolha um nome: ")
				cur.execute("SELECT * FROM funcionario, medico WHERE Nome='"+entry+"' AND funcionario.ID=medico.ID;")
				print(cur.fetchall())
	else:
		print("Entrada não válida\n")

db.close()