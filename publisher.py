# Alunos:
# Tiago Bachiega de Almeida     RA:628247
# Victor Tavares    RA:618042
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

	for comp in range(len(comp_list)):
		message = message + comp_list[comp] + " : " + str(random.uniform(0.1, 50.0)) + "\n"

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
		print "%d#%s#\n%s" % (share_update_id, topic, message)
		# Envia os dados da bolsa e de suas empresas para os subscribers interessados
		# O topico eh a respectiva bolsa.
		# Estamos usando # como separador de informacoes
		socket.send("%s#%d#\n%s" % (topic, share_update_id, message))
		# Atualiza o valor da atualizacao
		share_update_id = share_update_id + 1
		time.sleep(0.1)

def main():
	# Dicionario com as bolsas de valores e suas respectivas empresas
	market_companies = {'NYSE': ('BRK', 'BABA', 'JNJ', 'JPM', 'V'),
			'NASDAQ': ('MSFT', 'AAPL', 'AMZN', 'GOOGL', 'FB'),
			'TSE': ('7203', '9984', '9943', '6861', '9437'),
			'SSE': ('601398', '601318', '601857', '601288', '601988'),
			'HKEX': ('0700', '0941', '1299', '0883', '0016'),
			'EURONEXT': ('MC', 'ABI', 'FP', 'OR', 'SAN'),
			'LSE': ('RDSA', 'HSBA', 'UN', 'BP', 'BHP'),
			'SZSE': ('000858', '000002', '000333', '002415', '000651'),
			'TSX': ('RY', 'TD', 'ENB', 'BNS', 'CNR'),
			'BSE': ('RELIANCE', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'ITC'),
			'IBOVESPA': ('PETR4', 'ITUB4', 'BBDC4', 'VALE3', 'ABEV3')}

	# Cria um processo para tratar de cada bolsa de valores
	# Os processos irao executar a funcao pub 
	for market in market_companies:
		comp_list = market_companies[market]
		Process(target=pub, args=(market,comp_list)).start()

if __name__ == '__main__':
	main()