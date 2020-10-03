# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050

#Para rodar o codigo eh necessario utilizar python 2

from multiprocessing import Process
import zmq
import random
import sys
import time
import datetime
import json
import pickle

# Dicionario global com as salas a serem monitoradas e seus respectivos codigos
rooms = {"A":"LE1",
		"B":"LE2",
		"C":"LE3",
		"D":"LE4",
		"E":"LE5",
		"F":"LE6",
		"G":"PPGCC1",
		"H":"PPGCC2",
		"I":"PPGCC3",
		"J":"PPGCC4"}

# Esta funcao gera um valor aleatorio de temperatura para uma sala
# passada como parametro. Com isso, monta uma mensagem do tipo
# "Nome_da_sala : temperatura" eh gerada
def set_message(topic):
	val = random.uniform(10.0, 35.0)
	# message = str(rooms[topic]) + " : " + str(val) + "\n"
	json_data = {"sala":str(rooms[topic]),"topic":str(topic), "temp":str(val) ,"timestamp":str(datetime.datetime.now())}
	json_obj = json.dumps(json_data)
	return str(topic) + ":" + str(json_obj)
 
# Funcao do publisher.
# Cada publisher representa uma sala de aula do DC.
# O parametro topic eh a sala representada por este publisher
def pub(topic):

	# Realiza a conexao com o proxy
	port = "5559"
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	#socket.connect("tcp://localhost:%s" % port)
	socket.connect("tcp://127.0.0.1:%s" % port)
	#socket.connect('tcp://192.168.1.111:4507')

	# Identificador das atualizacoes dos valores de temperatura.
	# Utilizado para verificar se as temperaturas estao sendo atualizadas de forma igual em todos
	# os subscribers.
	room_update_id = 0

	# Loop infinito
	while True:
		# Gera uma mensagem com a funcao mostrada acima para o topico especifico
		message = set_message(topic)
		print(message)

		#Mostra as informacoes geradas
		print "%d#%s#%s#\n" % (room_update_id, topic, message)
		
		# Envia os dados acima e de suas empresas para os subscribers interessados no topico
		socket.send(message)
		print("############ENVIOU###############")
		
		# Atualiza o valor da atualizacao
		room_update_id = room_update_id + 1
		time.sleep(0.1)

# Função principal
def main():

	# Cria um processo para tratar de sala de aula
	# Os processos irao executar a funcao pub descrita acima
	for r in rooms:
		print("Starting process for room:", r)
		print(type(r))
		Process(target=pub, args=(r,)).start()

if __name__ == '__main__':
	main()
