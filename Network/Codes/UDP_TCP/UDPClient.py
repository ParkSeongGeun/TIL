# socket module이다. 이 module을 통해 소켓을 생성할 수 있다.
from socket import *

#서버의 IP 혹은 서버의 호스트 이름을 할당한다.
serverName = 'localhost'

# 목적지 port 번호를 나타낸다.
serverPort = 2000

# 클라이언트 소켓을 생성한다. AF_INET은 IPv4를 사용하고 있음을 나타내고, SOCK_DGRAM은 UDP 소켓임을 의미한다.
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 보낼 메시지를 입력 받는다.
message = input('Input lowercase sentence:')

# 소켓으로 바이트 형태를 보내기 위해 먼저 encode()를 통해 바이트 타입으로 변환한다.
# sendTo() 메서드는 목적지 주소를 메시지에 붙이고 그 패킷을 프로세스 소켓인 clientSocket으로 보낸다.
# 클라이언트 주소도 같이 보내지는데 이는 자동으로 수행된다.
clientSocket.sendto(message.encode(),(serverName, serverPort))

# 패킷 데이터는 modifiedMessage에 저장되고, 패킷의 출발지 주소(IP, port)는 serverAddress에 할당된다.
# recvfrom() 메서드는 2048의 버퍼 크기로 받아들인다. 
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# 출력
print(modifiedMessage.decode())

# 소켓 닫기
clientSocket.close()