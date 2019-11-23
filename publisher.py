# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050
import zmq
import random
import sys
import time
from multiprocessing import Process

# Esta funcao recebe a lista de empresas da bolsa em questao 
# e gera um numero aleatorio para o valor de cada acao de cada
# empresa desta lista. Com isso, monta uma mensagem do tipo
# <codigo da empresa> : <valor da acao>
def set_message(comp_list):

	message = ""
	message = message + " : " + str(random.uniform(10.0, 35.0)) + "\n"

	return message
 
# Funcao do publisher.
# Cada publisher representa uma bolsa de valores. Por exemplo, IBOVESPA, EURONEXT, etc.
# O parametro topic eh a bolsa representada por este publisher e comp_list eh a lista
# de empresas que estao nesta bolsa
def pub(topic, comp_list):

	# Realiza a conexao atraves do proxy
	port = "5559"
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.connect("tcp://localhost:%s" % port)

	# Identificador das atualizacoes dos valores das acoes. Usamos isto para
	# verificar se as acoes estao sendo atualizadas de forma igual em todos
	# os subscribers. Basta verificarmos o numero das acoes e os valores.
	share_update_id = 0

	# Processo principal do publiser
	while True:
		# Gera uma mensagem com valores aleatorios das acoes para cada empresa
		# no formato:
		# <codigo da empresa 1> : <valor da acao atual>
		# <codigo da empresa 2> : <valor da empresa atual>
		# ....
		message = set_message(comp_list)
		print("%d#%s#\n%s" % (share_update_id, topic, message))
		# Envia os dados da bolsa e de suas empresas para os subscribers interessados
		# O topico eh a respectiva bolsa.
		# Estamos usando # como separador de informacoes
		socket.send("%s#%d#\n%s" % (topic, share_update_id, message))
		# Atualiza o valor da atualizacao
		share_update_id = share_update_id + 1
		time.sleep(0.1)

def main():
	# Dicionario com as bolsas de valores e suas respectivas empresas
	salas = {1: '0', 
						2: '0', 
						3: '0', 
						4: '0', 
						5: '0', 
						6: '0', 
						7: '0', 
						8: '0',
						9: '0', 
						10: '0', 
						11: '0', 
						12: '0',
						13: '0', 
						24: '0', 
						15: '0'}


	# Cria um processo para tratar de cada bolsa de valores
	# Os processos irao executar a funcao pub 
	for item in salas:
		comp_list = salas[item]
		Process(target=pub, args=(item,comp_list)).start()

if __name__ == '__main__':
	main()