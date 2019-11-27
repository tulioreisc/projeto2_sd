# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050
import sys
import zmq
from multiprocessing import Process
import os
import time

# Funcao do subscriber. Cada subscriber eh um cliente
# que gostaria de monitorar determinada bolsa de valores.
# A bolsa escolhida eh o topico do subscriber, passado como
# argumento em topicfilter
def sub(topicfilter):

	# Conecta com os publishers atraves do proxy
	port = "5560"
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect ("tcp://localhost:%s" % port)
	socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

	# Este procedimetno eh usado para criar o log dos valores lidos da acao.
	# Para cada cliente sera gerado um arquivo de log com os valores das acoes
	# que ele leu acompanhado dos IDs desta remessa de valores.
	# Usaremos estes arquivos para compara se, para todos os IDs iguais entre os
	# clientes, os valores das acoes eh o mesmo, verificando se a sincronizacao
	# do sistema esta garantida.
	# Aqui, estamos apenas criando um arquivo diferente para cada cliente. O arquivo
	# tera um nome no formado <sub_log_<numero do arquivo - ordem de entrada do cliente>.txt"
	log_id = 0
	while(os.path.exists('sub_log_' + str(log_id) + '.txt') is True):
		log_id = log_id + 1
	log_file = open('sub_log_' + str(log_id) + '.txt', 'a')

	# Procedimento principal do cliente (quem vai monitorar)
	while True:
		# Recebe os valores do publisher escolhido
	    string = socket.recv()
	    # Obtem cada informacao realizando o split com o separador #
	    topic, share_update_id, messagedata = string.split("#")

	    # Mostra as informacoes na tela e as escreve no log
	    print("Share Market: " + str(topic))
	    file.write(log_file, "Share Market: " + str(topic) + "\n")
	    print("Share Update ID: " + str(share_update_id))
	    file.write(log_file, "Share Update ID: " + str(share_update_id) + "\n")
	    print("Companies:")
	    file.write(log_file, "Companies:")
	    print(messagedata)
	    file.write(log_file, messagedata + "\n")
	    time.sleep(0.1)
	    os.system('clear')

	log_file.close()

def main():

	# Menu inicial
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
	topicfilter = input("Escolha a sala que deseja monitorar a temperatura: ")

	# Inicia um processo para o subscriber
	process = Process(target=sub, args=(topicfilter,))
	process.start()
	process.join()


if __name__ == '__main__':
	main()