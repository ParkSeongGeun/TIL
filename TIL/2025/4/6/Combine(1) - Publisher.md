# Combine(1) - Publisher

| Publisher             |                                            | Subscriber        |
| --------------------- | ------------------------------------------ | ----------------- |
| 1. 그냥 존재하고 있음 |                                            |                   |
|                       | ← 2. Publisher에게 값 요청하면 달라고 말함 | subscriber 호출   |
|                       | 3. 알겠다고 함 →                           | subscription 전달 |
|                       | ← 4. 값을 달라고 함                        | request 호출      |
|                       | 5. subscriber가 원하는 만큼 값을 줌        | emit value        |
|                       | 6. completion을 전달함                     | emit completion   |

```swift
//
//  main.swift
//  CombinePractice
//
//  Created by 박성근 on 4/6/25.
//

import Foundation
import Combine

class IntSubscriber: Subscriber {
  typealias Input = Int
  typealias Failure = Never

  // Publisher가 Subscription 주면 호출됨
  func receive(subscription: any Subscription) {
    subscription.request(.max(1))
  }

  // Publisher가 주는 값을 처리
  func receive(_ input: Int) -> Subscribers.Demand {
    print("Received value: \(input)")

    // Publisher에게 한 번 더 달라고 요청
    return .max(1)
  }

  func receive(completion: Subscribers.Completion<Never>) {
    print("Received Completion: \(completion)")
  }
}

let intArray: [Int] = [1,2,3,4,5]

let intSubscriber = IntSubscriber()

intArray.publisher.subscribe(intSubscriber)
```

1. 먼저 정수 배열 `[1,2,3,4,5]`를 선언
2. `IntSubscriber` 클래스를 정의
   - 이 클래스는 Combine의 `Subscriber` 프로토콜을 준수하며, 정수 값을 받아 처리하도록 설계되어 있습니다:
     - `typealias Input = Int`: 이 Subscriber는 Int 타입의 입력을 받음
     - `typealias Failure = Never`: 이 Subscriber는 에러가 발생하지 않는 스트림을 구독
3. `receive(subscription:)` 메서드:
   - Publisher가 Subscription을 제공할 때 호출
   - `subscription.request(.max(1))`: 최초에 한 개의 값을 요청
4. `receive(_:)` 메서드:
   - Publisher가 값을 보낼 때마다 호출
   - 받은 값을 출력하고, 추가로 한 개의 값을 더 요청(`.max(1)`).
5. `receive(completion:)` 메서드:
   - 스트림이 완료되면 호출
   - 완료 신호를 출력
6. `intArray.publisher.subscribe(intSubscriber)`:
   - 배열에서 publisher를 생성하고, `intSubscriber`를 구독자로 등록
   - 배열의 각 요소가 순차적으로 Subscriber에게 전달

<br>

**실행 흐름:**

1. Publisher와 Subscriber 간의 연결 설정
2. Subscriber가 `.max(1)`로 첫 번째 값 요청
3. Publisher가 첫 번째 값(1)을 전송
4. Subscriber가 값을 받아 출력하고 다음 값을 요청
5. 이 과정이 배열의 모든 요소에 대해 반복
6. 배열의 모든 요소 처리 후 완료 신호 전송

---

### Publisher

```swift
public protocol Publisher<Output, Failure> {
    associatedtype Output
    associatedtype Failure : Error
    func receive<S>(subscriber: S) where S : Subscriber, Self.Failure == S.Failure, Self.Output == S.Input
}
```

**주요 구성 요소**

1. 제네릭 타입 매개변수
   - Output: Publisher가 방출하는 값의 타입
   - Failure: Publisher가 발생시킬 수 있는 에러 타입 (에러가 없으면 Never 사용)
2. 핵심 메서드
   - receive(subscriber:): Subscriber를 연결하는 메서드
   - Publisher 프로토콜을 구현하는 모든 타입에서 반드시 구현

<br>

**동작 방식**

1. 구독(Subscription)
   - subscribe(\_:) 또는 sink 등의 메서드를 통해 Subscriber를 Publisher에 연결
2. 구독 설정
   - Publisher는 `receive(subscriber:)` 메서드에서 Subscription 객체를 생성하여 Subscriber에게 제공
   - 어 근데 아까는 `subscribe(_:)` 이걸 쓰라고 했는데… 맞음.
     - 인터페이스 분리, 일관성 유지, 추상화 레벨을 위함
     ```swift
     extension Publisher {
         public func subscribe<S>(_ subscriber: S) where S : Subscriber, Self.Failure == S.Failure, Self.Output == S.Input
     }
     ```
3. 데이터 흐름
   - Subscriber가 `request(_:)` 메서드로 값을 요청하면
   - Publisher는 `receive(_:)` 메서드를 통해 값을 Subscriber에게 전달
   - 모든 값이 전달되거나 에러가 발생하면 `receive(completion:)`을 호출하여 스트림을 종료

<br>

**요약**

Publisher는 자신을 Subscribe 한 Subscriber에게 값을 내보내는 프로토콜

<br>

**종류**

- Deffered
- Empty
- Fail
- Future
- Just

---

### Subscriber

```swift
public protocol Subscriber<Input, Failure> : CustomCombineIdentifierConvertible {
    associatedtype Input
    associatedtype Failure : Error
    func receive(subscription: any Subscription)
    func receive(_ input: Self.Input) -> Subscribers.Demand
    func receive(completion: Subscribers.Completion<Self.Failure>)
}
```

**주요 구성 요소**

1. 제네릭 타입 매개변수
   - Input: Subscriber가 받을 수 있는 값의 타입
   - Failure: Subscriber가 처리할 수 있는 에러의 타입
2. 핵심 메서드
   - receive(subscription:)
     - Publisher로부터 구독 설정을 받을 때 호출됨
   - receive(\_:)
     - Publisher로부터 값을 받을 때 호출됨
   - receive(completion:)
     - Publisher로부터 완료 신호를 받을 때 호출됨

<br>

**동작 방식**

1. 구독 설정
   - Publisher에 연결되면 receive(subscription:) 메서드가 호출됨
   - 이 메서드에서 Subscriber는 Subscription 객체를 받고, request(\_:) 메서드를 호출하여 데이터 요청
2. 데이터 수신
   - Publisher가 값을 보내면 `receive(_:)` 메서드가 호출됨
   - 이 메서드는 `Subscribers.Demand` 값을 반환하여 추가로 몇 개의 값을 더 받을지 지정
   - `.unlimited`: 무제한으로 값을 받음
   - `.max(n)`: 최대 n개의 값을 더 받음
   - `.none`: 추가 값을 요청하지 않음
3. 완료 처리
   - 모든 값이 전달되거나 에러가 발생하면 `receive(completion:)` 메서드가 호출됨
   - `Subscribers.Completion<Failure>` 타입의 매개변수는:
     - `.finished`: 정상적으로 완료됨
     - `.failure(error)`: 에러와 함께 완료됨

<br>

**주의**

- Publisher의 <Output, Failure> 타입과 Subscriber의 <Input, Failure> 타입이 동일해야 한다.

---

### Demand

- `receive(input:)` 가 반환하는 값은 Subscribers.Demand 타입이다.

> Subscriber가 Publisher로부터 얼마나 많은 데이터를 요청할지 제어하는 메커니즘을 제공

- 즉 Subscriber가 Publisher에게 값을 달라고 요청할 수 있는데 그런 요청을 한 횟수
  - 즉 아까 receive(input:)의 반환 타입이 Demand인데요, 이는 Publisher에게 몇 번 더 값을 달라고 요청할지에 대한 값

```swift
// Publisher가 주는 값을 처리
func receive(_ input: Int) -> Subscribers.Demand {
		print("Received value: \(input)")

		// Publisher에게 한 번 더 달라고 요청
		return .max(1)

		// Publisher에게 값을 더 이상 안줘도 된다고 알릴 땐
		// return .none

		// Publisher에게 계속 값을 달라고 할 땐
		// return .unlimited
}
```

---

### Subscription

> Publisher와 Subscriber를 연결하는 프로토콜

```swift
public protocol Subscription : Cancellable, CustomCombineIdentifierConvertible {
    func request(_ demand: Subscribers.Demand)
}
```

**구독 과정**

- Subscriber가 `.subscribe(_:)` 메서드로 Publisher에 연결됨
- Publisher가 Subscription 객체를 생성해 Subscriber의 `receive(subscription:)` 메서드에 전달
  - 즉, Subscription 객체는 알아서 생긴다.

<br>

**특징**

- 특정 Subscriber가 Publisher에 연결된 순간 설정되는 Identity가 있어서 한 번만 cancel할 수 있고 cancel하면 이전에 연결된 Subscriber들이 모두 해제
  - thread safe 해야 함.
  - Cancellable 프로토콜을 채택하기 때문

```swift
let subject = PassthroughSubject<Int, Never>()
let anyCancellable = subject
  .sink { completion in
    print("received completion: \(completion)")
  } receiveValue: { value in
    print("received value: \(value)")
  }

subject.send(1)
anyCancellable.cancel()
subject.send(2)
```

```swift
received value: 1
Program ended with exit code: 0
```

**클로저를 통해 cancel() 될 때 조정**

```swift
let subject = PassthroughSubject<Int, Never>()
let anyCancellable = subject
  .handleEvents(
    receiveCancel: {
      print("Cancel 불렀따~~~")
    }
  )
  .sink { value in
    print("Received value: \(value)")
  }

subject.send(1)
anyCancellable.cancel()
subject.send(2)
```

```swift
Received value: 1
Cancel 불렀따~~~
Program ended with exit code: 0
```

---

## 미리 구현된 Publisher

- Just, Future, Deferred, Empty, Fail, Record, AnyPublisher

### Just(Struct)

> 매우 간단하고 특화된 목적을 가진 Publisher 타입 중 하나.

- 자신을 subscribe 하는 Subscriber들에게 한 번에 값을 내보낸 뒤 finish 이벤트를 보냄

```swift
let just = Just("This is Output")

just
  .sink { completion in
    print("received completion: \(completion)")
  } receiveValue: { value in
    print("received value: \(value)")
  }
```

```swift
received value: This is Output
received completion: finished
Program ended with exit code: 0
```

**Failure는 정의안해도 됨?**

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public struct Just<Output> : Publisher {
    public typealias Failure = Never
    public let output: Output

    public init(_ output: Output)
    public func receive<S>(subscriber: S) where Output == S.Input, S : Subscriber, S.Failure == Just<Output>.Failure
}
```

- Never 타입으로 설정이 되어 있음

---

### Never?

> 정상적으로 리턴하지 않는 함수의 리턴 타입, 값이 없는 타입

- Combine에서는 Publisher가 오류를 생성하지 않는 경우 Never 타입으로 설정

---

### Future(Class)

> A publisher that eventually produces a single value and then finished or fails

- 하나의 결과를 **`비동기`**로 생성한 뒤 completion event를 보낸다.

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
final public class Future<Output, Failure> : Publisher where Failure : Error {
    public typealias Promise = (Result<Output, Failure>) -> Void

    public init(_ attemptToFulfill: @escaping (@escaping Future<Output, Failure>.Promise) -> Void)

    final public func receive<S>(subscriber: S) where Output == S.Input, Failure == S.Failure, S : Subscriber
}
```

- 특징
  - **비동기 작업 표현**
    - Future는 나중에 한 번 값을 생성하거나 에러를 발생시키는 비동기 작업을 표현
  - **단일 결과 방출**
    - Promise 콜백을 통해 성공(Output) 또는 실패(Failure)를 한 번만 방출하고 완료
  - **에러 처리 가능**
    - Just와 달리 Future는 에러를 발생시킬 수 있으며, Failure 타입 파라미터를 통해 에러 유형을 지정

<br>

- 왜 Class인가?
  - 비동기로 작동할 때 상태 저장 동작을 가능하게 하기 위해 Class로 구현

```swift
var subscriptions = Set<AnyCancellable>()
var emitValue: Int = 0
var delay: TimeInterval = 3

func createFuture() -> Future<Int, Never> {
  return Future<Int, Never> { promise in
    delay -= 1
    DispatchQueue.main.asyncAfter(deadline: .now() + delay) {
      emitValue += 1
      promise(.success(emitValue))
    }
  }
}

let firstFuture = createFuture()
let secondFuture = createFuture()
let thirdFuture = createFuture()

firstFuture
    .sink(receiveCompletion: { print("첫번째 Future Completion: \($0)") },
          receiveValue: { print("첫번째 Future value: \($0)") })
    .store(in: &subscriptions)

secondFuture
    .sink(receiveCompletion: { print("두번째 Future completion: \($0)") },
          receiveValue: { print("두번째 Future value: \($0)") })
    .store(in: &subscriptions)

thirdFuture
    .sink(receiveCompletion: { print("세번째 Future completion: \($0)") },
          receiveValue: { print("세번째 Future value: \($0)") })
    .store(in: &subscriptions)

thirdFuture
    .sink(receiveCompletion: { print("세번째 Future completion2: \($0)") },
          receiveValue: { print("세번째 Future value2: \($0)") })
    .store(in: &subscriptions)

RunLoop.main.run(until: Date(timeIntervalSinceNow: 5))
```

---

### Deferred (Struct)

> A publisher that awaits subscription before running the supplied closure to create a publisher for the new subscriber

- 새로운 Subcriber의 Publisher를 만들기 위해 제공된 클로저를 실행하기 전에 Subscription을 기다리는 Publisher
  - 즉, 생성 시점이 아닌 구독 시점에 실제 Publisher를 생성
- Deferred → 지연된
- 각 구독자가 subscribe할 때마다 createPublisher 클로저가 호출되어 새로운 Publisher 인스턴스가 생성됨

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public struct Deferred<DeferredPublisher> : Publisher where DeferredPublisher : Publisher {

    public typealias Output = DeferredPublisher.Output
    public typealias Failure = DeferredPublisher.Failure

    public let createPublisher: () -> DeferredPublisher
    public init(createPublisher: @escaping () -> DeferredPublisher)

    public func receive<S>(subscriber: S) where S : Subscriber, DeferredPublisher.Failure == S.Failure, DeferredPublisher.Output == S.Input
}
```

```swift
struct FodenPublisher: Publisher {
  typealias Output = String
  typealias Failure = Never

  func receive<S>(subscriber: S) where S : Subscriber, Never == S.Failure, String == S.Input {
    subscriber.receive("Hello I'm Foden")
    subscriber.receive(completion: .finished)
  }
}

print("deferred publisher 생성됨")
let deferred = Deferred { () -> FodenPublisher in
  print("FodenPublisher가 만들어짐\n")
  return FodenPublisher()
}

deferred
  .sink(receiveCompletion: { print($0) }, receiveValue: { print($0) })
```

```swift
deferred publisher 생성됨
FodenPublisher가 만들어짐

Hello I'm Foden
finished
Program ended with exit code: 0
```

- FodenPublisher는 sink를 통해 subscribe 했을 때 Deferred를 생성할 때 구현한 클로저에서 만들어짐
- lazy와 비슷하게 실제로 사용될 때 Publisher를 생성

<br>

---

### AnyPublisher

> A publisher that performs type erasure by wrapping another publisher

- 타입 소거(type erasure) 기능을 가진 Publisher 래퍼

<br>

**특징**

- 타입 소거(Type Erasure)
  - 원본 Publisher의 구체적인 타입 정보를 숨기고, Output과 Failure 타입만 노출
  - Combine을 사용하다 보면 여러 Operator를 사용하면서 여러 Publisher 타입이 생성될 수 있는데 이걸 간단하게 처리하기 위해 사용

```swift
// 구체적인 Publisher 타입 생성
let concretePublisher = Just(42)
    .map { $0 * 2 }
    .filter { $0 > 50 }

// AnyPublisher로 타입 소거
let erasedPublisher: AnyPublisher<Int, Never> = concretePublisher.eraseToAnyPublisher()

// 이제 erasedPublisher는 원본의 구체적인 타입 정보를 숨기고
// AnyPublisher<Int, Never> 타입으로만 노출됨
```

---

### Empty(Struct)

> A publisher that never publishes any values, and optionally finishes immediately

- 아무런 값도 내보내지 않고 즉시 completion 이벤트를 보낼지 선택할 수 있는 Publisher

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public struct Empty<Output, Failure> : Publisher, Equatable where Failure : Error {
    public init(completeImmediately: Bool = true)
    public init(completeImmediately: Bool = true, outputType: Output.Type, failureType: Failure.Type)
    public let completeImmediately: Bool

    public func receive<S>(subscriber: S) where Output == S.Input, Failure == S.Failure, S : Subscriber
}
```

**주요 메서드**

- `init(completeImmediately: Bool = true)`
  - completion 이벤트를 바로 보낼지만 결정
- `init(completeImmediately: Bool = true, outputType: Output.Type, failureType: Failure.Type)`
  - Empty를 Subscriber나 다른 Publisher에 연결할 때 사용
- completeImmediately는 Empty가 즉시 completion 되어야 하는지 여부를 나타냄

<br>

**특징**

- 값 방출 없음
  - 어떠한 Output도 방출하지 않음
- 완료 시점 제어
  - completeImmediately 매개변수를 통해 즉시 완료할지 여부를 결정할 수 있음
- 타입 파라미터만 활용
  - 실제 값을 방출하지 않지만, Output과 Failure 타입은 지정해야함.
- Equatable 준수
  - 두 Empty 인스턴스가 동일한 `completeImmediately` 값을 가지면 동일한 것으로 간주됨

<br>

**사용 예시**

```swift
let anyPublisher = [1, nil, 3].publisher
  .flatMap { value -> AnyPublisher<Int, Never> in
    if let value = value {
      return Just(value).eraseToAnyPublisher()
    } else {
      return Empty().eraseToAnyPublisher()
    }
  }.eraseToAnyPublisher()

anyPublisher
  .sink(
    receiveCompletion: { print("AnyPublisher completion: \($0)") },
    receiveValue: { print("value: \($0)") }
  )
```

- Just, Empty의 두 가지 타입을 DownStream에 내려줘야 하는 상황
  - Upstream과 Downstream은 Combine의 데이터 흐름 방향을 나타내는 개념
  - **Upstream (상류)**:
    - 데이터가 흘러나오는 소스 방향을 의미
    - Publisher가 값을 생성하고 방출하는 쪽
    - 코드에서는 `[1, nil, 3].publisher`가 최초의 Upstream
  - **Downstream (하류)**:
    - 데이터가 흘러가는 목적지 방향을 의미
    - Subscriber가 값을 받아 처리하는 쪽
    - 코드에서는 `sink` 메서드로 생성된 Subscriber가 최종 Downstream

<br>

---

### Fail (Struct)

> A publisher that immediately terminates with the specified error

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public struct Fail<Output, Failure> : Publisher where Failure : Error {
    public init(error: Failure)
    public init(outputType: Output.Type, failure: Failure)

    public let error: Failure
    public func receive<S>(subscriber: S) where Output == S.Input, Failure == S.Failure, S : Subscriber
}
```

<br>

이걸 활용해보면

```swift
enum FodenError: Error {
    case itIsNil
}

let anyPublisher = [1, nil, 3].publisher
    .flatMap { value -> AnyPublisher<Int, FodenError> in
        if let value = value {
            let just = Just(value).setFailureType(to: FodenError.self)
            return just.eraseToAnyPublisher()
        } else {
            return Fail<Int, FodenError>(error: .itIsNil).eraseToAnyPublisher()
        }
    }
    .sink(receiveCompletion: { print("Completion: \($0)") },
          receiveValue: { print("value: \($0)") }
    )
```

---

### Record (Struct)

> A publisher that allows for recording a series of inputs and a completion, for later playback to each subscriber

- 일련의 값과 완료 이벤트를 기록한 후 이를 구독자에게 재생할 수 있게 해줌
  - 즉, 각각의 Publisher가 나중에 내보낼 수 있도록 input, completion을 저장해두는 Publisher

<br>

```swift
// 성공 케이스: 값들과 정상 완료 기록
let successRecord = Record<Int, Never>(
    output: [1, 2, 3, 4, 5],
    completion: .finished
)

// 실패 케이스: 값들과 에러 완료 기록
let failureRecord = Record<Int, Error>(
    output: [1, 2],
    completion: .failure(NSError(domain: "TestError", code: 1, userInfo: nil))
)

// 구독하여 기록된 값 재생
successRecord
    .sink(
        receiveCompletion: { print("완료: \($0)") },
        receiveValue: { print("값: \($0)") }
    )
	    .store(in: &subscriptions)

// 출력:
// 값: 1
// 값: 2
// 값: 3
// 값: 4
// 값: 5
// 완료: finished
```

<br>

**특징**

- 값과 완료 이벤트 기록
  - 미리 정의된 값들의 시퀀스와 완료 이벤트를 저장
- 재생 기능
  - 저장된 값과 완료 이벤트를 구독자가 구독할 때마다 동일하게 재생
- 테스트와 모의 객체에 유용
  - 특히 테스트 환경에서 일관된 데이터 스트림을 제공하는 데 유용함

---

### Subject

> A publisher that exposes a method for outside callers to publish elements

- 데이터를 발행할 수 있는 Publisher의 일종

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public protocol Subject : AnyObject, Publisher {
    func send(_ value: Self.Output)
    func send(completion: Subscribers.Completion<Self.Failure>)
    func send(subscription: Subscription)
}

extension Subject Where Self.Output == Void {
    public func send()
}
```

<br>

**주요 메서드**

- `func send(_ value: Self.Output)`
  - Subject를 통해 새로운 값(Output 타입)을 발행
  - Subject를 구독하고 있는 모든 Subscriber들은 이 값을 받게 됨
    - Publisher 체인에 새 데이터를 주입하는 방법입니다.
- `func send(completion: Subscribers.Completion<Self.Failure>)`
  - Subject가 값 발행을 완료했음을 알립니다.
  - 완료는 두 가지 상태가 가능
    - `.finished`: 정상적으로 완료되었음을 의미
    - `.failure(Error)`: 오류와 함께 완료되었음을 의미
  - 완료 이벤트가 전송되면 Subject는 더 이상 값을 발행하지 않음
    - 구독자들에게 스트림이 종료되었음을 알림
- `func send(subscription: Subscription)`
  - Subject에 새 구독을 추가
  - `Subscription` 객체는 Publisher와 Subscriber 사이의 연결을 관리
    - 이를 통해 Subject는 백프레셔(backpressure) 관리나 구독 취소 같은 구독 관련 기능을 제어
- `extension Subject Where Self.Output == Void { public func send() }`
  - Output 타입이 `Void`인 Subject에 대해 추가 편의성을 제공
    - 이 경우 값 없이 `send()`를 호출할 수 있으며, 이는 `send(())` (빈 튜플 전송)와 동일
    - 이는 값이 중요하지 않고 이벤트 자체가 중요한 경우(예: 버튼 탭, 타이머 틱 등)에 유용

<br>

**정리**

- Subject는 외부에서 Publisher 체인에 값을 주입할 수 있게 해주는 특별한 Publisher 유형
- 일반적으로 `PassthroughSubject` 나 `CurrentValueSubject` 같은 구체적인 구현체로 사용

---

### CurrentValueSubject

> A subject that wraps a single value and publishes a new element whenever the value changes

- CurrentValueSubject는 PassthroughSubject와 다르게 가장 최근에 published 된 값의 버퍼를 유지
- `send(_:)` 를 호출하면 현재 값도 업데이트돼서 값을 직접 업데이트하는 거랑 동일한 효과를 얻을 수 있음

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
final public class CurrentValueSubject<Output, Failure> : Subject where Failure : Error {
    final public var value: Output

    public init(_ value: Output)

    final public func receive<S>(subscriber: S) where Output == S.Input, Failure == S.Failure, S : Subscriber

    final public func send(subscription: Subscription)
    final public func send(_ input: Output)
    final public func send(completion: Subscribers.Completion<Failure>)
}
```

<br>

**사용 예시**

```swift
let currentValueSubject = CurrentValueSubject<String, Never>("Foden 첫번째 값")

// AnyCancellable 배열에 구독을 저장
var subscriptions = Set<AnyCancellable>()

currentValueSubject
    .sink(receiveCompletion: { print("1 번째 sink completion: \($0)") },
          receiveValue: { print("1 번째 sink value: \($0)") })
    .store(in: &subscriptions)  // 구독 저장

currentValueSubject
    .sink(receiveCompletion: { print("2 번째 sink completion: \($0)") },
          receiveValue: { print("2 번째 sink value: \($0)") })
    .store(in: &subscriptions)  // 구독 저장

currentValueSubject
    .sink(receiveCompletion: { print("3 번째 sink completion: \($0)") },
          receiveValue: { print("3 번째 sink value: \($0)") })
    .store(in: &subscriptions)  // 구독 저장

// 현재 Subscriber들에게 모두 보냄
currentValueSubject.send("Foden 두번째 값")
currentValueSubject.send(completion: .finished)

print(currentValueSubject.value)
```

```swift
1 번째 sink value: Foden 첫번째 값
2 번째 sink value: Foden 첫번째 값
3 번째 sink value: Foden 첫번째 값
2 번째 sink value: Foden 두번째 값
1 번째 sink value: Foden 두번째 값
3 번째 sink value: Foden 두번째 값
2 번째 sink completion: finished
1 번째 sink completion: finished
3 번째 sink completion: finished
Foden 두번째 값
```

<br>

**특징**

- 구독 취소
  - 개별 구독만 영향을 받으며, 다른 구독은 계속 값을 수신
- Subject 완료
  - 모든 구독에 영향을 미치며, 이후에는 값 발행이 불가능
- 완료 후 구독
  - 완료된 Subject를 구독해도 즉시 완료 신호만 받고 어떤 값도 받지 않음

---

### PassthroughSubject

> A subject that broadcasts elements to downstream subscribers

- `PassthroughSubject`는 `CurrentValueSubject`와 달리 값을 저장하지 않고 단순히 값을 전달
- 이벤트 기반 시스템에서 이벤트를 발행하는 데 적합

```swift
@available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
final public class PassthroughSubject<Output, Failure> : Subject where Failure : Error {

    public init()

    final public func receive<S>(subscriber: S) where Output == S.Input, Failure == S.Failure, S : Subscriber

    final public func send(subscription: Subscription)
    final public func send(_ input: Output)
    final public func send(completion: Subscribers.Completion<Failure>)
}
```

<br>

**주요 특징**

- **값 저장 없음**
  - 현재 값을 저장하지 않음
- **구독 시 초기값 없음**
  - 새 구독자는 구독 이후에 발행되는 값만 받음
- **값 접근 속성 없음**
  - `CurrentValueSubject`와 달리 `value` 속성이 없음

<br>

**사용 예시**

```swift
import Combine

// PassthroughSubject 생성 (초기값 없음)
let passthroughSubject = PassthroughSubject<String, Never>()

// 첫 번째 구독 설정
let firstSubscription = passthroughSubject
    .sink(receiveCompletion: { print("1번째 sink completion: \($0)") },
          receiveValue: { print("1번째 sink value: \($0)") })

// 첫 번째 값 발행
passthroughSubject.send("Haaland 첫번째 값")

// 두 번째 구독 설정 (첫번째 값 이후에 구독)
let secondSubscription = passthroughSubject
    .sink(receiveCompletion: { print("2번째 sink completion: \($0)") },
          receiveValue: { print("2번째 sink value: \($0)") })

// 두 번째 값 발행 (모든 구독자에게 전달)
passthroughSubject.send("Haaland 두번째 값")

// 세 번째 구독을 설정하고 즉시 취소
let thirdSubscription = passthroughSubject
    .sink(receiveCompletion: { print("3번째 sink completion: \($0)") },
          receiveValue: { print("3번째 sink value: \($0)") })
    .cancel()

// 세 번째 값 발행 (취소된 구독자에게는 전달되지 않음)
passthroughSubject.send("Haaland 세번째 값")

// 완료 신호 발행
passthroughSubject.send(completion: .finished)

// 완료 후 값 발행 (전달되지 않음)
passthroughSubject.send("Haaland 네번째 값")
```

```swift
1번째 sink value: Haaland 첫번째 값
2번째 sink value: Haaland 두번째 값
1번째 sink value: Haaland 두번째 값
2번째 sink value: Haaland 세번째 값
1번째 sink value: Haaland 세번째 값
2번째 sink completion: finished
1번째 sink completion: finished
```

<br>

**주요 특징**

- 구독 시 이전 값 수신 안함
  - 첫 번째 구독자는 "Haaland 첫번째 값"을 받지만, 두 번째 구독자는 이 값을 받지 않음
    - 두 번째 구독자는 구독 시점 이후의 값만 받음
  - `CurrentValueSubject`와의 핵심 차이점
- 취소된 구독
  - 세 번째 구독자는 `cancel()`로 인해 어떤 값도 받지 않음
- 완료 후 동작
  - 완료 신호 이후에 발행된 "Haaland 네번째 값"은 어떤 구독자에게도 전달되지 않음
  - 모든 활성 구독자는 완료 신호를 수신
- 저장된 값 없음
  - `PassthroughSubject`는 값을 저장하지 않으므로 `value` 속성이 없음
  - `CurrentValueSubject`와 달리 마지막 값에 접근할 방법이 없음

---
