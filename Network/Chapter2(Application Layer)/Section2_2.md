## 2.2 웹과 HTTP

### 2.2.1 HTTP 개요

- `HTTP`
  - 웹의 Application Layer Protocol
  - 두 가지 프로그램으로 구현된다.
    - Client / Server
  - 서로 HTTP 메시지를 교환하여 통신한다.
  - 즉, HTTP는 메시지의 구조, 클라이언트와 서버가 메시지를 어떻게 교환하는지에 대해 정의하고 있다.
- Web Page
  - 객체들로 구성된다.
    - 객체? → 단순히 URL로 지정할 수 있는 하나의 파일
  - 각 URL은 2개의 요소, 즉 객체를 갖고 있는 서버의 host name과 객체의 path name을 가지고 있따.
    > http://www.someSchool.edu/someDepartment/picture.gif
  - www.someSchool → Host name
  - /someDepartment/picture.gif → Path name
- HTTP는 웹 client → 웹 server에게 웹 페이지를 어떻게 요청하는지와 서버가 클라이언트로 어떻게 웹 페이지를 전송하는지를 정의한다.
- TCP를 transport protocol로 사용한다.
  - HTTP 클라이언트는 먼저 서버에 TCP 연결을 시작한다.
    - 일단 연결이 이뤄지면, 브라우저와 서버 프로세스는 그들의 socket interface 통해 TCP로 접속한다.
  - client는 HTTP 요청 메시지를 socket interface로 보내고 socket interface로부터 HTTP 응답 메시지를 받는다.
  - HTTP 서버는 socket interface로부터 요청 메시지를 받고 응답 메시지를 socket interface로 보낸다.
  - 클라이언트가 메시지를 socket interface로 보내면, 메시지는 클라이언트의 손을 떠난 것이고 TCP의 손에 쥐어진 것이다.
    - 메시지는 클라이언트의 손을 떠난 것이고 TCP의 손에 쥐어진 것이다.
      - 메시지가 궁극적으로 서버에 잘 도착한다는 것.
  - HTTP는 데이터의 손실 또는 TCP가 어떻게 손실 데이터를 복구하고 네트워크 내부에서 데이터를 올바른 순서로 배열하는지 걱정할 필요가 없다.
    - TCP, protocol stack의 하위 계층들이 하는 일이다.
- HTTP 서버는 클라이언트에 대한 정보를 유지하지 않으므로, HTTP를 stateless protocol이라고 한다.

---

### 2.2.2 비지속 연결, 지속 연결

**애플리케이션, 어떻게 이용되는지에 따라 일련의 요구가 계속해서, 일정 한 간격으로 주기적으로 혹은 간헐적으로 만들어질 수 있다.**

- client ↔ server의 상호작용이 TCP상에서 발생할 때 개발자는 아래의 결정을 해야한다.
  > 각 request/response 쌍이 분리된 TCP 연결을 통해 보내져야 하는지, 모든 요구와 해당하는 응답들이 같은 TCP 연결상으로 보내져야 하는지?
  - 전자 → non-persistent connection
  - 후자 → persistent connection (Default)

---

**Non-persistent connection HTTP**

(HTTP/1.0은 이를 지원한다.)

- 웹 페이지를 서버에서 클라이언트로 전송하는 단계를 아래의 예로 알아보자.
  → 페이지가 **기본 HTML 파일과 10개의 이미지**로 구성되고, 이 11개의 객체가 같은 서버에 있다.
- 연결 수행 과정은 아래와 같다.
  1. HTTP 클라이언트는 `HTTP 기본 포트 80`을 통해 서버로 `TCP 연결`을 시도한다.
     - TCP 연결과 관련하여 클라이언트와 서버에 각각 소켓이 있게 된다.
  2. HTTP 클라이언트는 설정된 TCP 연결 소켓을 통해 서버로 HTTP 요청 메시지를 보낸다.
     - 이 요청에 객체 경로도 포함된다.
  3. HTTP 서버는 TCP 연결 소켓을 통해 요청 메시지를 받는다.
     - 저장 장치로부터 경로의 객체를 추출한다.
     - HTTP 응답 메시지에 그 객체를 캡슐화 하여 소켓을 통해 클라이언트로 보낸다.
  4. HTTP 서버는 TCP에게 연결을 끊으라고 한다.
     - 실제로는 클라이언트가 응답 메시지를 올바로 받을 때까지 끊지 않는다.
  5. HTTP 클라이언트가 응답 메시지를 받으면, TCP 연결이 중단된다.
     - 메시지는 캡슐화된 객체가 HTML 파일인 것을 나타낸다.
     - 클라이언트는 응답 메시지로부터 파일을 추출하고 HTML 파일을 조사하여 10개의 JPEG 객체에 대한 참조를 찾는다.
  6. 참조되는 JPEG 객체에 대해 1 ~ 4단계를 반복한다.
- HTTP는 통신 프로토콜만 정의할 뿐, 웹 페이지에 대한 관심은 없다.
  - 브라우저는 웹 페이지를 수신하면서, 사용자에게 그 페이지를 보여준다.
- 앞 단계는 서버가 객체를 보낸 후 각 TCP 연결이 끊어지므로 비지속 연결을 사용하고 있따.
  - 연결이 다른 객체를 위해 유지되지 않는다.
  - HTTP/1.0은 non-persistent connection을 지원한다.
  - 그래서 해당 예에서는 사용자가 웹 페이지를 요청할 때 11개의 TCP 연결이 이뤄진다.
    - 사실 사용자가 동시성 정도를 조절하거나, 브라우저가 여러 TCP 연결을 설정하여 응답 시간을 줄일 수 있다.

**그래서 총 응답시간은?**

- 웹 브라우저, 서버 사이에서 TCP 연결을 시도할 때
  ![3-way handshake](../images/2_2_1.png)
  - ‘three-way handshake’를 포함한다.
  - 즉, 클라이언트가 작은 TCP 메시지를 서버로 보내고, 서버는 작은 메시지로 응답하고, 마지막으로 클라이언트가 다시 서버에게 응답한다.
    - 처음 두 부분이 경과하면 하나의 RTT가, handshake의 처음 두 과정이 끝난 후에 클라이언트는 HTTP 요청 메시지를 TCP 연결로 보내면서 handshake의 세 번째 부분(응답)을 함께 보낸다.
    - 일단 요청 메시지가 서버에 도착하면 서버는 HTML 파일을 TCP 연결로 보낸다.
      - 여기서도 RTT 하나를 필요로 한다.
  - 즉, 총 응답시간은 2\*RTT + (HTML 파일 서버가 전송하는 데 걸리는 시간) 이다.

**Persistent connection HTTP**

- 위에서 본 non-persistent connection 의 단점은 뭘까?

  - **각 요청 객체에 대한 새로운 연결이 설정되고 유지되어야 한다.**
    - TCP 버퍼가 할당되어야 하고, TCP 변수들이 클라이언트와 서버 양쪽에 유지되어야 한다.
    - 이는 수많은 클라이언트들의 요청을 동시에 서비스하는 웹 서버에는 심각한 부담이다.
  - 각 객체는 2RTT를 필요로 한다.

- HTTP/1.1 persistent connection에서 서버는 응답을 보낸 후에 TCP 연결을 그대로 유지한다.
  - 같은 client ↔ server 간의 이후 요청, 응답은 같은 연결을 통해 보내진다.
- HTTP의 디폴트 모드는 파이프라이닝을 이용한 persistent connection을 사용한다.

---

### 2.2.3 HTTP 메시지 format

**HTTP 요청 메시지**

![HTTP Request message](../images/2_2_2.png)

- SP (Space): 필드명과 값을 구분하는 공백 문자 (ASCII 32)
- Value: 헤더 필드의 실제 값
- CR (Carriage Return): 줄의 끝을 나타내는 제어 문자 (ASCII 13)
- LF (Line Feed): 새 줄의 시작을 나타내는 제어 문자 (ASCII 10)

**HTTP 응답 메시지**

![HTTP Respond message](../images/2_2_3.png)

- Status Code
  - 200 OK: 요청이 성공했고, 정보가 응답으로 보내졌다.
  - 301 Moved Permanently: 요청 객체가 영원히 이동되었다. 이때, 새로운 URL은 응답 메시지의 Location 헤더에 나와있다.
  - 400 Bad Request : 서버가 요청을 이해할 수 없다.
  - 404 Not Found : 요청한 문서가 서버에 존재하지 않는다.
  - 505 HTTP Version Not Supported : 요청 HTTP 프로토콜 버전을 서버가 지원하지 않는다.

---

### 2.2.4 사용자와 서버 간의 상호작용: 쿠키

- HTTP 서버는 stateless 하다.
  - 그러나 서버가 사용자 접속을 제한하거나 사용자에 따라 콘텐츠를 제공하기 원하므로 웹사이트가 사용자를 확인하는 것이 바람직할 때가 있다.
  - 이 목적으로 HTTP는 `쿠키(cookie)` 를 사용한다.
    [사이트가 사용자를 추적하게 해준다.]

![Cookie](../images/2_2_4.png)

- 쿠키 기술은 4가지 요소를 포함한다.
  - HTTP 응답 메시지 쿠키 헤더 라인
  - HTTP 요청 메시지 쿠키 헤더 라인
  - 사용자의 브라우저에 사용자 end point와 관리를 지속시키는 쿠키 파일
  - 웹사이트의 백엔드 DB
- 위의 그림은 내가 PC로 처음으로 아마존닷컴에 접속하는 상황을 가정한다.
  - 동작은 아래와 같이 이루어진다.
  1. 웹 서버에 `HTTP 요청 메시지`를 전달한다.
  2. 웹 서버는 유일한 식별 번호를 만들고 이 식별 번호로 인덱싱 되는 백엔드 데이터 베이스 안에 엔트리를 만든다.
  3. **HTTP 응답 메시지에** `Set-cookie: 식별 번호`의 헤더를 포함해서 전달한다.
  4. 브라우저는 헤더를 보고, 관리하는 특정한 쿠키 파일에 그 라인을 덧붙인다.
  5. 다시 **동일 웹 서버에 요청을 보낼 때**브라우저는 쿠키 파일을 참조하고 이 사이트에 대한 식별번호를 발췌하여 `Cookie : 식별 번호`의 헤더를 요청과 함께 보낸다.
