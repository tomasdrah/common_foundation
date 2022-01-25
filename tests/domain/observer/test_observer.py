from common_foundation.domain.observer import BasicObserverSubject, BasicObserver


def test_observer():
    called_1 = []
    called_2 = []

    def fce_to_call(value: str):
        called_1.append(1)
        assert value == "hello"

    def fce_to_call2(value: str):
        called_2.append(1)
        assert value == "by"

    observer_subject: BasicObserverSubject[str] = BasicObserverSubject(BasicObserver)

    first_observer = observer_subject.attach_fce(fce_to_call)
    observer_subject.notify("hello")
    observer_subject.detach(first_observer)

    second_observer = observer_subject.attach_fce(fce_to_call2)
    observer_subject.notify("by")
    observer_subject.detach(second_observer)

    assert called_1
    assert called_2
