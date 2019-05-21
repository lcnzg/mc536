#!/usr/bin/python3
import pymysql
import os
from data_gen import generate_database

clear = lambda: os.system('cls')

# Open database connection
db = pymysql.connect("localhost", "jonathas", passwd="EiC9Shei", db="mc536")

cur = db.cursor()

setup_commands = generate_database()

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

clear()

while 1:
	print("Escolha o tipo de usuário:\n\t1 - Médico\n\t2 - Enfermeiro\n\t3 - Paciente\nPara sair escolha 0")
	entry = input("Escolha um número: ")

	if (entry == '0'):
		break;
	elif (entry == '1'):
		clear()
		while(1):
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar todos os médicos\n\t2 -Consultar médicos por nome\nPara sair escolha 0")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break;
			elif (entry == '1'):
				entry = input("Escolha um nome: ")
				print(entry)
				cur.execute("SELECT * FROM funcionario WHERE Nome='"+entry+"';")
				print(cur.fetchall())
	elif (entry == '2'):
		while(1):
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar todos os médicos\n\t2 -Consultar médicos por nome\nPara sair escolha 0")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break;
			elif (entry == '1'):
				entry = input("Escolha um nome: ")
				cur.execute("SELECT * FROM funcionario, medico WHERE Nome='"+entry+"' AND funcionario.ID=medico.ID;")
				print(cur.fetchall())
	elif (entry == '3'):
		while(1):
			print("Escolha o tipo de consulta a fazer:\n\t1 - Consultar todos os médicos\n\t2 -Consultar médicos por nome\nPara sair escolha 0")
			entry = input("Escolha um número: ")
			if (entry == '0'):
				break;
			elif (entry == '1'):
				entry = input("Escolha um nome: ")
				cur.execute("SELECT * FROM funcionario, medico WHERE Nome='"+entry+"' AND funcionario.ID=medico.ID;")
				print(cur.fetchall())
	else:
		print("Entrada não válida\n")

db.close()