# Alunos:
# Tiago Bachiega de Almeida     RA:628247
# Victor Tavares    RA:618042
import zmq

def main():

    context = zmq.Context(1)
    
    # Gera as conexoes do frontned
    frontend = context.socket(zmq.XSUB)
    frontend.bind("tcp://*:5559")
    
    # Gera as conexoes do backend
    backend = context.socket(zmq.XPUB)
    backend.bind("tcp://*:5560")

    # Realiza o proxy entre o frontend e o backend
    zmq.proxy(frontend, backend)

if __name__ == "__main__":
    main()