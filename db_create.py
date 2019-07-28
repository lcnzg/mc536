#!/usr/bin/python3
import pymysql
import os
from data_gen import generate_database

# Cria comando para limpar tela do terminal do windows
clear = lambda: os.system('cls')

def is_empty(struct):
	if(struct):
		return False
	else:
		return True

def imprimir_resposta(response, header):
	if (response):
		width_res = max(len(str(word)) for row in response for word in row)
		width_header = max(len(str(word)) for row in header for word in row)
		col_width = max(width_res, width_header) + 2
		
		for row in header:
			print ("".join(str(word).ljust(col_width) for word in row))
		print()
		for row in response:
			print("".join(str(word).ljust(col_width) for word in row))
		input("Aperte Enter ao terminar")
	else:
		input("Nenhum registro encontrado. Aperte Enter para retornar")



# Open database connection
print("Conectanto ao banco")
db = pymysql.connect("localhost", "jonathas", passwd="EiC9Shei", db="mc536")

cur = db.cursor()

setup_commands = generate_database()

cur.execute("SELECT * FROM medico;")
response = cur.fetchall()
if(len(response) >= 20):
	entry = input("Existem tabelas preenchidas, deseja criar novas? (y/n): ")
	if (entry.lower == 'y'):
		print("Limpando tabelas")
		cur.execute("DROP TABLE IF EXISTS ajuda_em;") 
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

		print("Gerando dados")
		for command in setup_commands:
			cur.execute(command)

		print("Submetendo comandos")
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
		cur.execute("SELECT id FROM medico WHERE id="+medId+";")
		if(is_empty(cur.fetchall())):
			input("Medico nao encontrado. Pressione Enter para voltar")
			continue

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Cirurgias\
				\n\t2 - Pacientes cadastrados\
				\n\t3 - Exames pedidos\
				\n\t4 - Diagnósticos feitos\
				\n\t5 - Consultas realizadas\
				\n\t6 - Internações\
				\n\t7 - Funcionários\
				\n\t0 - Para retornar")
			entry = input("Escolha um número: ")

			if (entry == '0'):
				break

			# Caso escolha cirurgia
			elif (entry == '1'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Cirurgias sob sua responsabilidade\
					\n\t2 - Enfermeiros ajudantes em cirurgia\
					\n\t0 - Para retornar")
				entry = input("Escolha um número: ")
				if (entry == '0'):
					continue

				elif (entry == '1'):
					cur.execute("SELECT cirurgia.ncirurgia, paciente.nome, idsala, tipo, data, horario FROM funcionario\
						INNER JOIN realiza_cirurgia ON realiza_cirurgia.ID=funcionario.ID\
						INNER JOIN cirurgia ON cirurgia.ncirurgia=realiza_cirurgia.ncirurgia\
						INNER JOIN paciente ON cirurgia.cpf=paciente.cpf\
						WHERE funcionario.ID="+medId+"\
						ORDER BY data;")

					header = [["ID Cirurgia", "Paciente", "Sala", "Tipo", "Data", "Horário"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '2'):
					ncirurgia = input("Escolha ID da cirurgia: ")
					cur.execute("SELECT nome FROM funcionario, enfermeiro, ajuda_em\
						WHERE ncirurgia="+ncirurgia+" AND enfermeiro.id=funcionario.id\
						AND enfermeiro.id=ajuda_em.id;")

					header = [["Nome"]]
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
						FROM Paciente WHERE Nome LIKE'%"+nomePaciente+"%';")
					
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
				cur.execute("SELECT paciente.Nome, Tipo, Data, Horario, Local FROM funcionario\
					INNER JOIN Exame ON Exame.ID_medico=funcionario.ID\
					INNER JOIN paciente ON paciente.cpf=exame.cpf\
					WHERE funcionario.id="+medId+";")

				header = [["Nome", "Tipo", "Data", "Horário", "Sala"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar diagnósticos feitos
			elif (entry == '4'):
				print("Escolha o tipo de consulta:\
					\n\t1 - Diagnósticos dados\
					\n\t2 - Número de diagnósticos por patologia\
					\n\t0 - Para sair escolha")
				entry = input("Escolha um numero: ")
				if (entry == '0'):
					continue

				elif (entry == '1'):				
					cur.execute("SELECT Paciente.Nome, Patologia, SIntomas FROM funcionario\
						INNER JOIN Diagnostico ON Diagnostico.IDmedico=funcionario.ID\
						INNER JOIN paciente ON paciente.cpf=diagnostico.cpf\
						WHERE funcionario.ID="+medId+";")

					header = [["Nome", "Patologia", "Sintomas"]]
					imprimir_resposta(cur.fetchall(), header)
				
				elif (entry == '2'):
					entry = input("Escolha uma patologia: ")
					cur.execute("SELECT COUNT(*) FROM Diagnostico WHERE patologia = '"+entry+"';")
					header = [["Numero de diagnosticos de "+entry]]
					imprimir_resposta(cur.fetchall(), header)

			elif (entry == '5'):
				cur.execute("SELECT paciente.Nome, data FROM funcionario\
					INNER JOIN consulta ON consulta.ID=funcionario.ID\
					INNER JOIN paciente ON paciente.cpf=consulta.cpf\
					WHERE funcionario.ID="+medId+"\
					ORDER BY data;")

				header = [["Nome", "Data"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar internação de paciente
			elif (entry == '6'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Consultar lista de internações\
					\n\t2 - Consultar internação por CPF\
					\n\t3 - Consultar internação por nome\
					\n\t4 - Consultar numero de pacientes com certa patologia\
					\n\t5 - Constular numero de pacientes em certa sala\
					\n\tPara sair escolha 0")
				entry = input("Escolha um numero: ")

				if (entry == '0'):
					continue
				
				elif (entry == '1'):
					cur.execute("SELECT nome, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
						ORDER BY data_entrada;")
					
					header = [["Paciente", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '2'):
					cpfPaciente = input("Escolha CPF: ")
					cur.execute("SELECT nome, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
						WHERE Paciente.CPF='"+cpfPaciente+"';")
				
					header = [["Paciente", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '3'):
					nomePaciente = input("Escolha o nome do paciente: ")
					cur.execute("SELECT nome, paciente.cpf, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
						WHERE Paciente.Nome LIKE '%"+nomePaciente+"%';")
				
					header = [["Paciente", "CPF", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '4'):
					patologia = input("Escolha a patologia: ")
					cur.execute("SELECT paciente.cpf, nome, datanascimento, genero, tiposang FROM\
						internacao, paciente, diagnostico WHERE internacao.cpf = paciente.cpf AND\
						diagnostico.cpf = paciente.cpf and patologia='"+patologia+"';")
					header = [["CPF", "Nome", "Data Nascimento", "Genero", "Tipo" "Sanguineo"]]	
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '5'):
					idsala = input("Escolha a sala: ")
					cur.execute("SELECT idsala FROM sala WHERE sala.idsala="+idsala+";")
					if(is_empty(cur.fetchall())):
						input("Sala nao encontrada. Pressione Enter para retornar")
						continue
					cur.execute("SELECT Count(CPF) FROM internacao WHERE internacao.idsala="+idsala+";")
					header = [["Numero de pacientes na sala "+str(idsala)]]	
					imprimir_resposta(cur.fetchall(), header)

			elif (entry == '7'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Médicos\
					\n\t2 - Enfermeiros\
					\n\tPara sair escolha 0")
				entry = input("Escolha un numero: ")
					
				if (entry == '0'):
					continue

				elif (entry == '1'):
					cur.execute("SELECT nome, cpf, crm, especialidade FROM medico\
						INNER JOIN funcionario ON medico.id = funcionario.id;")

					header = [["Nome", "CPF", "CRM", "Especialidade"]]
					imprimir_resposta(cur.fetchall(), header)
					
				elif (entry == '2'):
					cur.execute("SELECT enfermeiro.ID, nome, cpf, setor FROM enfermeiro\
						INNER JOIN funcionario ON enfermeiro.id = funcionario.id;")

					header = [["ID", "Nome", "CPF", "Setor"]]
					imprimir_resposta(cur.fetchall(), header)

			else:
				input("Entrada inválida. Tente novamente")
				continue

	# Caso seja enfermeiro
	elif (entry == '2'):
		enfId = input("Digite seu ID: ")
		cur.execute("SELECT id FROM enfermeiro WHERE id="+enfId+";")
		if(is_empty(cur.fetchall())):
			input("Enfermeiro nao encontrado. Pressione Enter para voltar")
			continue

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Cirurgias\
				\n\t2 - Pacientes cadastrados\
				\n\t3 - Internações\
				\n\t4 - Funcionários\
				\n\t0 - Para sair")
			entry = input("Escolha um número: ")

			if (entry == '0'):
				break

			# Caso escolha cirurgia
			elif (entry == '1'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Cirurgias nas quais ajuda\
					\n\t2 - Enfermeiros ajudantes em cirurgia\
					\n\t0 - Para retornar")
				entry = input("Escolha um número: ")
				if (entry == '0'):
					continue

				elif (entry == '1'):
					cur.execute("SELECT cirurgia.ncirurgia, paciente.nome, idsala, tipo, data, horario FROM funcionario\
						INNER JOIN ajuda_em ON ajuda_em.ID=funcionario.ID\
						INNER JOIN cirurgia ON cirurgia.ncirurgia=ajuda_em.ncirurgia\
						INNER JOIN paciente ON cirurgia.cpf=paciente.cpf\
						WHERE funcionario.ID="+enfId+"\
						ORDER BY data;")

					header = [["ID Cirurgia", "Paciente", "Sala", "Tipo", "Data", "Horário"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '2'):
					ncirurgia = input("Escolha ID da cirurgia: ")
					cur.execute("SELECT nome FROM funcionario, enfermeiro, ajuda_em\
						WHERE ncirurgia="+ncirurgia+" AND enfermeiro.id=funcionario.id\
						AND enfermeiro.id=ajuda_em.id;")

					header = [["Nome"]]
					imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar paciente por nome
			elif (entry == '2'):
				nomePaciente = input("Digite o nome desejado: ")
				cur.execute("SELECT nome, cpf, datanascimento, genero, tiposang\
					FROM Paciente WHERE Nome LIKE '%"+nomePaciente+"%';")
				
				header = [["Nome", "CPF", "Data Nascimento", "Gênero", "Tipo Sanguíneo"]]
				imprimir_resposta(cur.fetchall(), header)

			# Caso escolha consultar internação de paciente
			elif (entry == '3'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Consultar lista de internações\
					\n\t2 - Consultar internação por CPF\
					\n\t3 - Consultar internação por nome\
					\n\t0 - Para sair")
				entry = input("Escolha um numero: ")

				if (entry == '0'):
					continue
				
				elif (entry == '1'):
					cur.execute("SELECT nome, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF;")
					
					header = [["Paciente", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '2'):
					cpfPaciente = input("Escolha CPF: ")
					cur.execute("SELECT nome, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
						WHERE Paciente.CPF='"+cpfPaciente+"';")
				
					header = [["Paciente", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

				elif (entry == '3'):
					nomePaciente = input("Escolha o nome do paciente: ")
					cur.execute("SELECT nome, paciente.cpf, idsala, data_entrada, data_alta FROM Paciente\
						INNER JOIN Internacao ON Internacao.CPF=Paciente.CPF\
						WHERE Paciente.Nome LIKE '%"+nomePaciente+"%';")
				
					header = [["Paciente", "CPF", "Sala", "Data de entrada", "Data de alta"]]
					imprimir_resposta(cur.fetchall(), header)

			elif (entry == '4'):
				print("Escolha o tipo de consulta a fazer:\
					\n\t1 - Médicos\
					\n\t2 - Enfermeiros\
					\n\t0 - Para sair")
				entry = input("Escolha un numero: ")
					
				if (entry == '0'):
					continue

				elif (entry == '1'):
					cur.execute("SELECT nome, cpf, crm, especialidade FROM medico\
						INNER JOIN funcionario ON medico.id = funcionario.id;")

					header = [["Nome", "CPF", "CRM", "Especialidade"]]
					imprimir_resposta(cur.fetchall(), header)
					
				elif (entry == '2'):
					cur.execute("SELECT nome, cpf, setor FROM enfermeiro\
						INNER JOIN funcionario ON enfermeiro.id = funcionario.id;")

					header = [["Nome", "CPF", "Setor"]]
					imprimir_resposta(cur.fetchall(), header)
			
			else:
				input("Entrada inválida. Tente novamente")
				continue

	# Caso seja paciente
	elif (entry == '3'):
		cpfPaciente = input("Digite seu CPF: ")
		cur.execute("SELECT cpf FROM paciente WHERE cpf="+cpfPaciente+";")
		if(is_empty(cur.fetchall())):
			input("Paciente nao encontrado. Pressione Enter para voltar")
			continue

		while(1):
			clear()
			print("Escolha o tipo de consulta a fazer:\
				\n\t1 - Cirurgias\
				\n\t2 - Internação\
				\n\t3 - Exames\
				\n\t4 - Diagnósticos\
				\n\t5 - Consultas\
				\n\t0 - Para sair")
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
			
			# Caso escolha consultas
			elif (entry == '5'):
				cur.execute("SELECT funcionario.nome, data FROM paciente\
					INNER JOIN consulta ON paciente.CPF=consulta.CPF\
					INNER JOIN funcionario ON funcionario.id=consulta.id\
					WHERE paciente.CPF='"+cpfPaciente+"'\
					ORDER BY data;")
			
				header=[["Médico responsável", "Data"]]
				imprimir_resposta(cur.fetchall(), header)

			else:
				input("Entrada inválida. Tente novamente")
				continue

	else:
		input("Entrada inválida. Tente novamente")

db.close()