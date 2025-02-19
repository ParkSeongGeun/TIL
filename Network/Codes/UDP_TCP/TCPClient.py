from socket import *

serverName = 'localhost'
serverPort = 2000

# 클라이언트 소켓을 의미한다. SOCK_STREAM으로 TCP 소켓임을 명시했다.
# UDP 때와 마찬가지로 따로 출발지 주소를 명시하지 않는다. (운영체제가 대신 해준다.) 
clientSocket = socket(AF_INET, SOCK_STREAM)

# 클라이언트가 TCP 소켓을 이용하여 서버로 데이터를 보내기 전에 TCP 연결이 먼저 클라이언트와 서버 사이에 설정되어야 한다.
# 해당 라인으로 TCP 연결을 시작하고, connect() 메서드의 파라미터는 연결의 서버 쪽 주소이다.
# 이 라인이 수행된 후에 3-way handshake가 수행되고 클라이언트와 서버 간에 TCP 연결이 설정된다.
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence:')

# 클라이언트 소켓을 통해 TCP 연결로 보낸다. UDP 소켓처럼 패킷을 명시적으로 생성하지 않으며 패킷에 목적지 주소를 붙이지 않는다.
# 대신 클라이언트 프로그램은 단순히 문자열에 있는 바이트를 TCP 연결에 제공한다.
clientSocket.send(sentence.encode())

# 서버로부터 바이트를 수신하기를 기다린다.
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())

# 연결을 닫는다. 이는 클라이언트 TCP가 서버의 TCP에게 TCP 메시지를 보내게 한다.
clientSocket.close()