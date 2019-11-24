# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050

#Para rodar o codigo eh necessario utilizar python 2

import zmq
import random
import sys
import time
from multiprocessing import Process

# Dicionario global com as salas a serem monitoradas e seus respectivos codigos
rooms = {"1":"LE1",
	"2":"LE2",
	"3":"LE3",
	"4":"LE4",
	"5":"LE5",
	"6":"LE6",
	"7":"PPGCC1",
	"8":"PPGCC2",
	"9":"PPGCC3",
	"10":"PPGCC4",
	"11":"Auditorio",
	"12":"Almoxarifado",
	"13":"Sala de Banco de dados",
	"14":"Secretaria",
	"15":"Sala de reuniao"}

# Esta funcao gera um valor aleatorio de temperatura para uma sala
# passada como parametro. Com isso, monta uma mensagem do tipo
# "Nome_da_sala : temperatura" eh gerada
def set_message(topic):
	message = str(rooms[topic]) + " : " + str(random.uniform(10.0, 30.0)) + "\n"
	return message
 
# Funcao do publisher.
# Cada publisher representa uma sala de aula do DC.
# O parametro topic eh a sala representada por este publisher
def pub(topic):

	# Realiza a conexao com o proxy
	port = "5559"
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.connect("tcp://localhost:%s" % port)

	# Identificador das atualizacoes dos valores de temperatura.
	# Utilizado para verificar se as temperaturas estao sendo atualizadas de forma igual em todos
	# os subscribers.
	room_update_id = 0

	while True:
		# Gera uma mensagem com a funcao mostrada acima para o topico especifico
		message = set_message(topic)

		#Mostra as informacoes geradas
		print "%d#%s#\n%s" % (room_update_id, topic, message)
		
		# Envia os dados acima e de suas empresas para os subscribers interessados no topico
		socket.send("%s#%d#\n%s" % (topic, room_update_id, message))
		
		# Atualiza o valor da atualizacao
		room_update_id = room_update_id + 1
		time.sleep(0.1)

def main():

	# Cria um processo para tratar de sala de aula
	# Os processos irao executar a funcao pub descrita acima
	for r in rooms:
		Process(target=pub, args=(r)).start()

if __name__ == '__main__':
	main()