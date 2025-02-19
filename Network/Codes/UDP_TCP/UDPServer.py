from socket import *

# 포트 번호
serverPort = 2000

# UDP 소켓 생성
serverSocket = socket(AF_INET, SOCK_DGRAM)

# 12000 포트 번호를 소켓에 할당한다. 이를 통해 서버 IP 주소의 12000 포트로 패킷을 보내면 해당 소켓으로 패킷이 전달된다.
serverSocket.bind(('', serverPort))

print("The server is ready to receive")

while True:
    # 패킷이 서버에 도착하면 데이터는 메세지에 할당되고 패킷의 출발지 주소는 clientAddress에 저장된다.
    # 해당 주소로 서버는 응답을 어디에 보내야할지 알 수 있다.
    message, clientAddress = serverSocket.recvfrom(2048)
    
    # 바이트 데이터를 decode()하고 대문자로 변환한다.
    modifiedMessage = message.decode().upper()
    
    # 클라이언트 주소를 대문자로 변환된 메시지에 붙이고, 그 결과로 만들어진 패킷을 서버에 보낸다.
    # 서버의 주소도 같이 보내지는데 이는 자동으로 수행된다.
    serverSocket.sendto(modifiedMessage.encode(), clientAddress) 