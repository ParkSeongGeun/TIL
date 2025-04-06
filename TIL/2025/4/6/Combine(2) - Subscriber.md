# Combine(2) - Subscriber

미리 정의된 Publisher와 같이 미리 정의된 Subscriber에는 뭐가 있을까?

---

### Sink (class)

> A simple subscriber that requests an unlimited number of values upon subscription

- Publisher로부터 값을 수신하는 기본적인 Subscriber 구현을 제공
- sink() 연산자를 사용할 때 내부적으로 생성되는 Subscriber

```swift
final public class Sink<Input, Failure> : Subscriber, Cancellable, CustomStringConvertible,
                                            CustomReflectable, CustomPlaygroundDisplayConvertible
where Failure : Error {
    final public var receiveValue: (Input) -> Void { get }
    final public var receiveCompletion: (Subscribers.Completion<Failure>) -> Void { get }

    final public var description: String { get }
    final public var customMirror: Mirror { get }
    final public var playgroundDescription: Any { get }

    public init(receiveCompletion: @escaping ((Subscribers.Completion<Failure>) -> Void),
                receiveValue: @escaping ((Input) -> Void))

    final public func cancel()

    // Subscriber 프로토콜의 필수요소들
    final public func receive(subscription: Subscription)
    final public func receive(_ value: Input) -> Subscribers.Demand
    final public func receive(completion: Subscribers.Completion<Failure>)
}
```

<br>

**주요 기능**

- Sink는 아래의 프로토콜을 구현
  - `Subscriber`: 값을 수신하기 위한 기본 프로토콜
  - `Cancellable`: 구독을 취소할 수 있는 기능
  - `CustomStringConvertible`, `CustomReflectable`, `CustomPlaygroundDisplayConvertible`: 디버깅과 시각화를 위한 프로토콜

<br>

**주요 속성, 메서드**

1. 속성
   - `receiveValue: (Input) -> Void`: 값을 수신할 때 실행될 클로저
   - `receiveCompletion: (Subscribers.Completion<Failure>) -> Void`: 완료 신호를 수신할 때 실행될 클로저
   - `description`, `customMirror`, `playgroundDescription`: 디버깅 표시용 속성들
2. 초기화

   ```swift
   public init(receiveCompletion: @escaping ((Subscribers.Completion<Failure>) -> Void),
               receiveValue: @escaping ((Input) -> Void))
   ```

   - 두 개의 클로저를 전달받아 초기화
     - 값을 처리할 클로저
     - 완료 신호를 처리할 클로저

3. Subscriber 프로토콜 구현 메서드

   ```swift
   final public func receive(subscription: Subscription)
   final public func receive(_ value: Input) -> Subscribers.Demand
   final public func receive(completion: Subscribers.Completion<Failure>)
   ```

   - `receive(subscription:)`: 구독 시작 시 호출되며, 내부적으로 `.unlimited` 수요를 요청
   - `receive(_:)`: 값 수신 시 호출되며, 제공된 `receiveValue` 클로저를 실행하고 `.none` 수요를 반환
   - `receive(completion:)`: 완료 신호 수신 시 호출되며, 제공된 `receiveCompletion` 클로저를 실행

4. Cancellable 프로토콜 구현 메서드

   ```swift
   final public func cancel()
   ```

   - 구독을 취소하는 메서드로, 호출 시 Publisher와의 연결을 종료하고 더 이상 값을 수신하지 않음.

<br>

**실제 사용 방법**

```swift
let cancellable = publisher.sink(
    receiveCompletion: { completion in
        switch completion {
        case .finished:
            print("정상 완료")
        case .failure(let error):
            print("오류 발생: \(error)")
        }
    },
    receiveValue: { value in
        print("값 수신: \(value)")
    }
)
```

---

### Assign (class)

> A simple subscriber that assigns received elements to a property indicated by a key path

- Publisher로부터 수신한 값을 특정 객체의 속성에 직접 할당하는 Subscriber
  - 데이터 바인딩을 간단하게 구현할 수 있도록 도와줌

```swift
final public class Assign<Root, Input> : Subscriber, Cancellable, CustomStringConvertible,
CustomReflectable, CustomPlaygroundDisplayConvertible {
    public typealias Failure = Never
    final public var object: Root? { get }
    final public let keyPath: ReferenceWritableKeyPath<Root, Input>

    public init(object: Root, keyPath: ReferenceWritableKeyPath<Root, Input>)

    final public func receive(subscription: Subscription)
    final public func receive(_ value: Input) -> Subscribers.Demand
    final public func receive(completion: Subscribers.Completion<Never>)

    final public func cancel()
}
```

<br>

**주요 속성**

- `object: Root?`: 값을 할당할 대상 객체 (취소 후에는 nil이 됨)
- `keyPath: ReferenceWritableKeyPath<Root, Input>`: 값을 할당할 객체의 속성 경로

<br>

**사용 예시**

```swift
class TemperatureViewModel {
    @Published var celsius: Double = 0
    var fahrenheit: Double = 32
}

let viewModel = TemperatureViewModel()

// celsius 속성 변경을 감시하여 fahrenheit 속성에 자동으로 변환된 값을 할당
let cancellable = viewModel.$celsius
    .map { celsius in
        return celsius * 9 / 5 + 32
    }
    .assign(to: \.fahrenheit, on: viewModel)

// celsius 값 변경 시 fahrenheit 값이 자동으로 업데이트됨
viewModel.celsius = 25 // fahrenheit는 77이 됨

print(viewModel.fahrenheit) // 77
```

---

### Demand (struct)

> A requested number of items, sent to a publisher from a subscriber through the subscription

- Subscriber가 subscription을 통해 Publisher에게 요청한 item의 수
  - 즉, 몇번이나 값을 요청했느냐에 대한 값
- Publisher와 Subscriber 사이의 데이터 흐름 제어를 위한 핵심 구조체

```swift
@frozen public struct Demand : Equatable, Comparable, Hashable, Codable,
CustomStringConvertible {
    public static let unlimited: Subscribers.Demand
    public static let none: Subscribers.Demand
    @inlinable public static func max(_ value: Int) -> Subscribers.Demand
}
```

**사용 예시**

```swift
class DemandTestSubscriber: Subscriber {
  typealias Input = Int
  typealias Failure = Never

  func receive(subscription: Subscription) {
    print("subscribe 시작")

    subscription.request(.max(1))
  }

  func receive(_ input: Int) -> Subscribers.Demand {
    print("receive input: \(input)")

    if input == 2 {
      return .max(1)
    } else {
      return .none
    }
  }

  func receive(completion: Subscribers.Completion<Never>) {
    print("receive completion: \(completion)")
  }
}

let publisher = [2, 3, 4, 5].publisher

publisher
  .print()
  .subscribe(DemandTestSubscriber())
```

```swift
receive subscription: ([2, 3, 4, 5])
subscribe 시작
request max: (1)
receive value: (2)
receive input: 2
request max: (1) (synchronous)
receive value: (3)
receive input: 3
```

---

### Completion (enum)

> A signal that a publisher doesn’t produce additional elements, either due to normal completion or an error

- 정상적인 완료 혹은 에러로 인해 Publisher가 값을 더 이상 생성하지 않는다는 신호

```swift
@frozen public enum Completion<Failure> where Failure : Error {
    case finished
    case failure(Failure)
}
```

<br>

**사용 예시**

```swift
// custom Error를 만듭니다.
enum FodenError: Error {
    case fodenLowCareer
}

class FodenSubscriber: Subscriber {
    typealias Input = Int
    typealias Failure = FodenError

    func receive(subscription: Subscription) {
        subscription.request(.unlimited)
    }

    func receive(_ input: Int) -> Subscribers.Demand {
        print("receive input: \(input)")
        return .none
    }

    func receive(completion: Subscribers.Completion<PinguError>) {
        // .fodenLowCareer 수신시 실행
        if completion == .failure(.pinguIsBaboo) {
            print("Foden는 하락세입니다.")
        } else {
            print("finished!")
        }
    }
}

let subject = PassthroughSubject<Int, FodenError>()
let subscriber = PinguSubscriber()

subject.subscribe(subscriber)

subject.send(100)
subject.send(completion: .failure(.FodenError))
subject.send(200)
```

```swift
receive input: 100
Foden는 하락세입니다.
```

---

### AnySubscriber

> A type-erasing subscriber

- 어떤 subscriber의 타입을 간단하게 사용할 수 있도록 래핑해주는 struct

```swift
let fodenSubscriber = FodenSubscriber()
let anySubscriber = AnySubscriber(fodenSubscriber)
```
