## 1.4 패킷 교환 네트워크에서의 지연, 손실과 처리율

- 컴퓨터 네트워크는 반드시 두 end point 간에 처리율(전달될 수 있는 초당 데이터의 양)을 제한하여 end point 간에 지연을 야기하며 실제로 패킷을 잃어버리기도 한다.
- 이 절에서는 컴퓨터 네트워크에서의 지연, 손실, 처리율을 조사하고 개량화한다.

### 1.4.1 패킷 교환 네트워크에서의 지연 개요

- packet이 path를 따라 한 노드(host || router)에서 다음 노드로 전달되므로 그 packet은 경로상의 각 노드에서 다양한 지연을 겪게 된다.
    - **노드 처리 지연(nodal processing delay)**
    - **큐잉 지연(queing delay)**
    - **전송 지연(transmission delay)**
    - **전파 지연(propagation delay)**
    
    **→ total node delay**
    
    ![image](https://github.com/user-attachments/assets/99627044-22c7-4b59-89df-e9041557be17)


**지연 유형**

- 라우터 A는 라우터 B에 이르는 `하나의 출력(outgoing) 링크`를 가지며, 이 링크 앞에 `큐(queue, 버퍼(buffer))`가 존재한다.
    - packet이 upstream node로부터 라우터 A에 도착
    - 라우터 A는 그 packet에 대한 적당한 출력 링크를 결정하기 위해 packet header를 조사
    - 라우터 A는 선택된 링크로 그 packet 전송
- 만약 링크가 이미 이용되고 있거나, queue에서 대기하는 packet이 있다면, queue로 들어간다.

**처리 지연**

- packet header를 조사하고, 어디로 보낼지를 결정하는 시간

**큐잉 지연**

- queue에 저장되어 link로 전송되기를 기다리는 다른 packet의 수에 의해 결정

**전송 지연**

- packet이 FIFO 방식으로 전송된다고 가정하면 packet은 다른 packet이 모두 전송된 다음에 전송된다.
    - packet의 길이를 L(bit)
    - 링크의 전송률을 R(bps)라고 하면
- 전송 지연은 L/R이다.

**전파 지연**

- d/s
    - d: 라우터 사이의 거리
    - s: 링크의 전파 속도

**전송 지연과 전파 지연 비교**

- 전송 지연은 router가 packet을 내보내는 데 필요한 시간
    - packet length / 링크 전송률의 함수
    - router 사이의 거리와는 상관 없음.
- 전파 지연은 bit가 router에서 router로 전파되는 데 걸리는 시간
    - 두 router 사이의 거리에 대한 함수, packet length / link transmission rate 와는 상관 없다.
- packet의 앞선 비트들이 packet의 나머지 다른 비트가 이전 router에서 전송되기를 기다리는 동안에 이미 다음 router에 도착할 수도 있다.

$$
d_{nodal} = d_{proc}+d_{queue}+d_{trans}+d_{prop}
$$

---

### 1.4.2 queing delay와 packet loss

- 다른 3가지 delay와 다르게 queing delay는 packet마다 다를 수 있다.
- 아래에 영향을 받는다.
    - 트래픽이 큐에 도착하는 비율, 링크의 전송률, 도착하는 트래픽의 특성
    - 즉 그 트래픽이 주기에 맞춰서 또는 burst하게 도착하느냐에 의해 주로 결정된다.

- 다음과 같은 상황을 가정하자.
    
    ```
    패킷이 큐에 도착하는 평균율 : a 패킷/초
    전송률(패킷이 큐에서 밀려나는 비율) : R 비트/초
    모든 패킷은 L 비트
    큐가 매우 커서 무한대 비트를 저장할 수 있음
    ```
    
    - 트래픽 강도(La/R)
        - L = 패킷 크기(비트)
        - a = 초당 패킷 도착률
        - R = 초당 처리 비트율
        - La = 초당 도착하는 총 비트 수
        - R = 초당 처리할 수 있는 비트 수
    - **La/R > 1인 경우**
        - 도착률이 처리율 초과
        - 큐가 무한정 증가
        - 지연시간 무한대로 증가
    - **La/R ≤ 1인 경우**
        - 도착 패턴에 따라 지연시간 달라짐
        - 주기적 도착: 큐잉 지연 없음
        - 버스트(집중) 도착: 큐잉 지연 발생
    - **예시**
        - L = 1000비트, R = 1Mbps, a = 900패킷/초
        - La/R = (1000×900)/(1×10^6) = 0.9
        - 트래픽 강도가 1 미만이므로 시스템 안정
- **트래픽 강도가 1보다 크지 않게 시스템을 설계하는 것이 중요**
    
    ![image 1](https://github.com/user-attachments/assets/f56fe214-835d-475d-adf9-9e1414c3f512)

    1. 트래픽 강도가 0에 가까울 경우
        - 패킷 도착이 드물고 간격이 멀어서 다음에 도착하는 패킷이 큐에서 다른 패킷을 발견하는 경우가 없다.
        - 따라서 평균 큐잉 지연은 0에 가까워진다.
    2. 트래픽 강도가 1에 가까울 경우
        - 패킷 도착이 전송용량을 초과하여 큐가 생성될 것이다.
        - 도착률이 전송률보다 작아질 때 큐의 길이가 줄어든다.

**packet loss**

- 실제론 queue size는 유한하다.
    - packet delay가 무한하진 않지만, 꽉 찬 것을 발견하는 경우 router는 해당 packet을 drop한다.
    - 즉, 해당 packet을 lost한다.
- queue에서의 overflow는 트래픽 강도가 1보다 클 때 상호작용 애니메이션에서 볼 수 있다.
- 이후 이야기를 하지만, lost packet은 모든 데이터가 궁극적으로 출발지에서 목적지까지 전달되었음을 보장하기 위해 end point들 간에 재전송될 수 있다.

---

### 1.4.3 종단 간 지연

$$
d_{end-end} = N(d_{proc}+d_{trans}+d_{prop})
$$

- N-1개의 router
- 각 router들의 processing delay는 d_proc
- 각 호스트와 출발지 호스트에서의 전송률은 R비트/초
- 각 링크에서의 전파 지연은 d_prop

**Traceroute**

- 네트워크 지연 진단 프로그램

**end point, application, and other delays**

- processing, transmission, propagation delay 이외에도 end point에서 중요한 지연이 더 있을 수 있다.
- 예로 공유 매체로 packet을 전송하고자 하는 end point는 다른 end point system과 매체를 공유하기 위해 프로토콜의 일부로 전송을 “의도적으로” 지연시킬 수 있다.
    - 6장에서 살펴본다.
- VoIP(Voice-over-IP) 애플리케이션에 있는 media packetization delay
    - packet을 encoding된 디지털 음성으로 채워야 한다.
    - 해당 시간을 의미한다.

### 1.4.4 컴퓨터 네트워크에서의 처리율

- delay, packet loss 외에 컴퓨터 네트워크에서의 또 다른 주요한 성능 수단은 end point들 간 처리율(throughput)이다.
- 컴퓨터 네트워크를 통해 호스트 A에서 호스트 B로 커다란 파일을 전송하는 상황을 생각해보자.
    - 해당 파일은 **F 비트**로 구성되며, 호스트 B가 파일의 모든 F 비트를 수신하는 데 **T초가 걸린다.**
    - 평균 처리율(average throughput)은 ***F/T***비트/초다.
- 다음 예를 보자.
    
    ![image 2](https://github.com/user-attachments/assets/3299dcf2-e8b2-408a-8a3b-89f126116380)

    - (a)는 2개의 end point.
        - 즉, 2개의 통신 링크와 router로 연결된 하나의 서버와 하나의 클라이언트다.
        - Rs: 서버와 router 간의 링크 속도
        - Rc: Router와 클라이언트 간의 링크 속도
    - **서버-클라이언트 처리율**은 얼마일까?
        - 비트는 유체(fluid), 통신 링크는 파이프(pipe)로 생각해보자
        - 서버는 Rs bps보다 빠른 속도로 링크상으로 비트를 내보낼 수 없고, 라우터는 Rc bps보다 빠른 속도로 비트를 전달할 수 없다.
        - 처리율 = min{Rc, Rs} = 병목 링크(bottleneck link)의 전송률이다.
        - 처리율을 결정했으므로 이제 F비트의 커다란 파일을 서버에서 클라이언트로 전송하는데 걸리는 시간으로 F/min{Rs, Rc}의 근삿값을 구할 수 있다.
    - (b)는 서버와 클라이언트 간에 N개의 링크를 가진 네트워크를 보여준다.
        - N개의 링크 전송률은 각각 R1, R2… Rn이다.
        - 처리율이 min{R1, R2, … , Rn} == 서버와 클라이언트 간 경로상의 병목 링크의 전송률
    
    ![image 3](https://github.com/user-attachments/assets/5c4369f9-4388-4365-b051-e9e8fe3628f6)

    - (a)는 컴퓨터 네트워크로 연결된 2개의 end point, 즉 서버와 클라이언트를 보여준다.
        - 서버로부터 클라이언트로의 파일 전송에 대한 처리율을 고려하자.
        - 출발지에서 목적지로 흐를 수 있는 비트 속도는 Rs와 Rc의 최솟값과 같다.
            - 처리율 = min{Rc, Rs}
    - (b)는 컴퓨터 네트워크의 코어에 연결된 10개의 서버와 10개의 클라이언트를 나타낸다.
        - 10개의 동시적인 다운로드가 일어나는 상황이다.
        - 10개의 다운로드가 통과하는 코어에 하나의 링크가 있다.
        - 이 링크 R의 전송률을 R이라고 하자.
        - 모든 서버 접속 링크가 같은 Rs의 속도를 가지며, 모든 클라이언트 접속 링크는 같은 Rc의 속도를 갖고, 코어에서의 모든 링크 전송률은 Rs, Rc, R보다 크다고 가정하자.
            - **케이스 정리**
                - **기본 설정:**
                    - 서버 10대, 클라이언트 10대가 각각 연결
                    - 중간에 하나의 공통 링크(R) 존재
                    - 각 서버는 Rs 속도로 전송 가능
                    - 각 클라이언트는 Rc 속도로 수신 가능
                - **처리율 결정 과정:**
                    1. **이상적인 경우:**
                        - 공통 링크 속도가 충분히 빠름
                        - 각자 자기 속도로 통신 가능
                        - 처리율 = min{Rs, Rc}
                        - 예: Rs=2Mbps, Rc=1Mbps면 1Mbps로 통신
                    2. **현실적인 경우:**
                        - 공통 링크가 병목현상 발생
                        - R=5Mbps를 10개가 나눠씀
                        - 각각 500kbps만 사용 가능
                        - 서버나 클라이언트가 더 빨라도 소용없음
                - **예시 상황:**
                    - Rs = 2Mbps (서버 속도)
                    - Rc = 1Mbps (클라이언트 속도)
                    - R = 5Mbps (공통 링크)
                    - 결과: 각 연결은 500kbps로 제한
                        - 이유: 5Mbps ÷ 10 = 500kbps
                        - 더 빠른 속도로 보내고 싶어도 불가능
