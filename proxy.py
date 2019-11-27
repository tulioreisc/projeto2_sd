# Autores
# Leonardo Utida Alcantara     RA: 628182
# Tulio Reis Carvalho    RA: 628050

#Para rodar o codigo eh necessario utilizar python 2

import zmq

def main():

    context = zmq.Context(1)
    
    # Gera as conexoes relacionadas ao frontned
    frontend = context.socket(zmq.XSUB)
    frontend.bind("tcp://*:5559")
    
    # Gera as conexoes relacionadas ao backend
    backend = context.socket(zmq.XPUB)
    backend.bind("tcp://*:5560")

    # Realiza o proxy entre o frontend e o backend
    zmq.proxy(frontend, backend)

if __name__ == "__main__":
    main()