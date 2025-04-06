# Combine(3) - Subscription

Publisher, Subscriber를 연결하는 역할을 하는 Subscription에 대해 알아보자.

---

### Subscription

> A protocol representing the connection of a subscriber to a publisher

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public protocol Subscription : Cancellable, CustomCombineIdentifierConvertible {
    func request(_ demand: Subscribers.Demand)
}
```

**특징**

- Subscription에는 특정 Subscriber가 Publisher를 subscribe 할 때 정의되는 ID가 있어서 Class로만 정의해야 함.

## <br>

### Cancellable

> A protocol indicating that an activity or action supports cancellation

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public protocol Cancellable {
    func cancel()
}

@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
extension Cancellable {
    @available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
    public func store<C>(in collection: inout C) where C : RangeReplaceableCollection, C.Element == AnyCancellable

    @available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
    public func store(in set: inout Set<AnyCancellable>)
}
```

<br>

**store(in:)**

- 취소 토큰을 컬렉션에 저장하는 편리한 메서드
- 두 가지 오버로드가 존재
  - 하나는 `RangeReplaceableCollection` 프로토콜을 준수하는 컬렉션에 저장
  - 다른 하나는 `Set<AnyCancellable>`에 특화된 버전

<br>

**정리**

- Subscription을 저장할 때 사용하는 메서드
- 타입은 AnyCancellable

---

### AnyCancellable

> A type-erasing cancellable object that executes a provided closure when canceled

- Cancellable 객체의 타입의 타입을 지운 것
- AnySubscriber, AnyPublisher와 비슷하게 모든 Cancellable도 AnyCancellable로 쉽게 처리할 수 있음

---

### Custom Combine Identifier COnvertible

> A protocol for uniquely identifying publisher streams

- Publisher Stream을 식별하기 위한 프로토콜
- 여러 개의 Subscription들이 연결된 Publisher 체인에서 이 프로토콜을 통해 Subscription을 식별할 수 있음

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public protocol CustomCombineIdentifierConvertible {
    var combineIdentifier: CombineIdentifier { get }
}
```

<br>

**사용 예시**

```swift
// 1. 기본 데이터 모델 (PinguPublisher의 YoutubeSubscriber와 같은 역할)
struct NumberData {
    let value: Int
}

// 2. 구독(Subscription) 구현
final class CustomSubscription<S: Subscriber>: Subscription where S.Input == NumberData, S.Failure == Never {
    private var requested: Subscribers.Demand = .none
    private var numbers: [NumberData]
    private var subscriber: S?
    private var currentIndex = 0

    init(subscriber: S, numbers: [NumberData]) {
        print("CustomSubscription 생성됨!")
        self.subscriber = subscriber
        self.numbers = numbers
    }

    func request(_ demand: Subscribers.Demand) {
        print("요청받은 demand: \(demand)")
        requested += demand

        // 요청된 demand만큼 값을 전달
        while requested > .none && currentIndex < numbers.count {
            if let subscriber = subscriber {
                let number = numbers[currentIndex]
                currentIndex += 1

                // 구독자에게 값을 전달하고, 반환된 demand를 추가
                let additionalDemand = subscriber.receive(number)
                print("값 전달 후 반환된 demand: \(additionalDemand)")
                requested += additionalDemand
                requested -= 1 // 하나의 값을 전달했으므로 demand 감소
            }
        }

        // 모든 값을 전달했으면 완료 통지
        if currentIndex >= numbers.count {
            subscriber?.receive(completion: .finished)
        }
    }

    func cancel() {
        print("CustomSubscription이 cancel됨!")
        numbers.removeAll()
        subscriber = nil
    }
}

// 3. 발행자(Publisher) 구현
extension Publishers {
    struct CustomPublisher: Publisher {
        var numbers: [NumberData]

        typealias Output = NumberData
        typealias Failure = Never

        func receive<S>(subscriber: S)
            where S: Subscriber, Failure == S.Failure, Output == S.Input {
            let subscription = CustomSubscription(subscriber: subscriber, numbers: numbers)
            subscriber.receive(subscription: subscription)
        }

        mutating func append(number: NumberData) {
            numbers.append(number)
        }
    }

    static func customNumbers(values: [Int]) -> Publishers.CustomPublisher {
        let numberData = values.map { NumberData(value: $0) }
        return Publishers.CustomPublisher(numbers: numberData)
    }
}

// 4. 구독자(Subscriber) 구현
class CustomDemandSubscriber: Subscriber {
    typealias Input = NumberData
    typealias Failure = Never

    func receive(subscription: Subscription) {
        print("구독 시작")
        // 처음에는 1개만 요청
        subscription.request(.max(1))
    }

    func receive(_ input: Input) -> Subscribers.Demand {
        print("receive input: \(input.value)")

        // value가 2인 경우만 추가로 1개 요청, 나머지는 추가 요청 없음
        if input.value == 2 {
            return .max(1)
        } else {
            return .none
        }
    }

    func receive(completion: Subscribers.Completion<Failure>) {
        print("receive completion: \(completion)")
    }
}

// 5. 사용 예
let numbersArray = [2, 3, 4, 5].map { NumberData(value: $0) }
let customPublisher = Publishers.CustomPublisher(numbers: numbersArray)

// 방법 1: 커스텀 구독자 사용
let subscriber = CustomDemandSubscriber()
customPublisher.subscribe(subscriber)

// 방법 2: sink 사용 (일반적인 방법)
var subscriptions = Set<AnyCancellable>()
Publishers.customNumbers(values: [2, 3, 4, 5])
    .sink(receiveCompletion: { print("sink completion: \($0)") },
          receiveValue: { print("sink value: \($0.value)") })
    .store(in: &subscriptions)

// 취소하기
for subscription in subscriptions {
    subscription.cancel()
}
```

```swift
CustomSubscription 생성됨!
구독 시작
요청받은 demand: max(1)
receive input: 2
값 전달 후 반환된 demand: max(1)
receive input: 3
값 전달 후 반환된 demand: max(0)
CustomSubscription 생성됨!
요청받은 demand: unlimited
sink value: 2
값 전달 후 반환된 demand: max(0)
sink value: 3
값 전달 후 반환된 demand: max(0)
sink value: 4
값 전달 후 반환된 demand: max(0)
sink value: 5
값 전달 후 반환된 demand: max(0)
sink completion: finished
```

<br>

1. 데이터 모델 (NumberData)

   ```swift
   struct NumberData {
       let value: Int
   }
   ```

<br>

2. 구독(Subscription)

- `requested` 변수로 요청된 값의 수를 추적
- `currentIndex`로 현재 처리 중인 값의 위치를 추적
- 구독자가 반환한 추가 demand를 처리
- 모든 값을 전달한 후에는 완료를 알림

<br>

3. 발행자(Publisher)

- `receive(subscriber:)` 메서드에서 구독을 설정
- 편의 메서드 `customNumbers(values:)`를 통해 쉽게 생성

<br>

4. 구독자(Subscriber) 구현

- 처음에는 1개의 값만 요청
- 값 2를 받으면 추가로 1개를 요청
- 다른 값을 받으면 추가 요청을 하지 않음

<br>

5. 사용 방법

- 커스텀 구독자를 직접 사용
- `sink`를 통한 일반적인 방식 사용
