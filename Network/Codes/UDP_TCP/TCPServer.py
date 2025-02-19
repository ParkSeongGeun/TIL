from socket import *

serverPort = 2000

# TCP 소켓 생성
serverSocket = socket(AF_INET, SOCK_STREAM)

# 서버의 포트 번호를 소켓과 연관시킨다.
serverSocket.bind(('', serverPort))

# 연관시킨 소켓은 대기하며 클라이언트가 문을 두드리기를 기다린다.
# 큐잉되는 연결의 최대 수를 나타낸다.
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    # 클라이언트가 TCP 연결 요청을 하면 accept() 메소드를 시작해서 클라이언트를 위한 연결 소켓을 서버에 생성한다.
    # 그 뒤 클라이언트와 서버는 핸드셰이킹을 완료해서 클라이언트의 소켓과 연결 소켓 사이의 TCP 연결을 생성한다.
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    
    # 응답을 보내고 연결 소켓을 닫는다. 그러나 환영소켓인 serverSocket이 열려있어 다른 클라이언트가 서버에 연결을 요청할 수 있다. 
    connectionSocket.close()