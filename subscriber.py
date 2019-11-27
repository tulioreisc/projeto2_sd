# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050

#Para rodar o codigo eh necessario utilizar python 2

import sys
import zmq
from multiprocessing import Process
import os
import datetime
import time
from statistics import mean 
import json
import pickle

# Funcao do subscriber. 
# Cada subscriber eh um cliente que gostaria de monitorar uma temperatura
# de sala de aula. A sala eh escolhida utilizando o parametro topicfilter
def sub(topicfilter):

	# Conecta com os publishers com o proxy
	port = "5560"
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect ("tcp://localhost:%s" % port)
	socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
	
	# Cria o o log dos valores lidos da acao. Para cada cliente sera gerado um 
	# arquivo de log com os valores de temperatura de sala que ele leu acompanhado dos 
	# IDs destes valores.
	# Usaremos estes arquivos para comparar se para todos os IDs iguais entre os
	# clientes, as temperaturas sao iguais, verificando se a sincronizacao esta garantida.
	log_id = 0
	while(os.path.exists('sub_log_' + str(log_id) + '.txt') is True):
		log_id = log_id + 1
	log_file = open('sub_log_' + str(log_id) + '.txt', 'a')


	cont = 0
	meanTemp = []
	while True:
		# Recebe os valores do publisher escolhido
		msg = socket.recv()
		msg = msg.split(':',1)[1]
		print(msg)
		json_data = json.loads(msg)

		#  Obtem cada informacao, realizando um split na json_data recebida
		# topic, update_id, timeStamp, val, messagedata = json_data.split("#")
		topic = json_data["topic"]
		timeStamp = json_data["timestamp"]	
		val = json_data["temp"]
		sala = json_data["sala"]
		if(cont<=10):
			print("Entrou no cont<10")
			meanTemp.append(float(val))
			# Mostra as informacoes na tela e as escreve no log
			print("Topic: " + str(topic))
			print("Sala: " + str(sala))
			print("Update ID: " + str(timeStamp))
			print("Temp: " + str(val))
			time.sleep(0.1)
			os.system('clear')
			cont = cont + 1
		else:
			print("Entrou no outro")
			meanTemp.append(float(val))
			meanTemp = meanTemp[1:]
			# Mostra as informacoes na tela e as escreve no log
			print("Topic: " + str(topic))
			file.write(log_file, "Topic: " + str(topic) + "\n")
			print("Sala: " + str(sala))
			file.write(log_file, "Sala: " + str(sala) + "\n")
			print("Update ID: " + str(timeStamp))
			file.write(log_file, "Update ID: " + str(timeStamp) + "\n")
			print("\nMedia de temp: " + str(mean(meanTemp)))
			file.write(log_file, str(mean(meanTemp)) + "\n")
			time.sleep(0.1)
			os.system('clear')
			cont = cont + 1

	log_file.close()

def main():

# Menu inicial mostrando as salas e seus respectivos IDs
	print("Opcao    Sala")
	print('A: LE1')
	print('B: LE2')
	print('C: LE3')
	print('D: LE4')
	print('E: LE5')
	print('F: LE6')
	print('G: PPGCC1')
	print('H: PPGCC2')
	print('I: PPGCC3')
	print('J: PPGCC4')

	# Selecao de topico
	topicfilter = raw_input("Escolha a sala de aula que deseja monitorar: ")

	# Inicia um processo para o subscriber
	process = Process(target=sub, args=(topicfilter,))
	process.start()
	process.join()


if __name__ == '__main__':
	main()