# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050

#Para rodar o codigo eh necessario utilizar python 2

import sys
import zmq
from multiprocessing import Process
import os
import time

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


	while True:
		# Recebe os valores do publisher escolhido
	    string = socket.recv()

	    # Obtem cada informacao, realizando um split na string recebida
	    topic, update_id, messagedata = string.split("#")

	    # Mostra as informacoes na tela e as escreve no log
	    print("Sala: " + str(topic))
	    file.write(log_file, "Sala: " + str(topic) + "\n")
	    print("Update ID: " + str(update_id))
	    file.write(log_file, "Update ID: " + str(update_id) + "\n")
	    print(messagedata)
	    file.write(log_file, messagedata + "\n")
	    time.sleep(0.1)
	    os.system('clear')

	log_file.close()

def main():

# Menu inicial mostrando as salas e seus respectivos IDs
	print("Opcao    Sala")
	print('1		LE1')
	print('2		LE2')
	print('3		LE3')
	print('4		LE4')
	print('5		LE5')
	print('6		LE6')
	print('7		PPGCC1')
	print('8		PPGCC2')
	print('9		PPGCC3')
	print('10		PPGCC4')
	print('11		Auditorio')
	print('12		Almoxarifado')
	print('13		Sala de Banco de dados')
	print('14		Secretaria')
	print('15		Sala de reuniao')

	# Selecao de topico
	topicfilter = raw_input("Escolha a sala de aula que deseja monitorar: ")

	# Inicia um processo para o subscriber
	process = Process(target=sub, args=(topicfilter,))
	process.start()
	process.join()


if __name__ == '__main__':
	main()