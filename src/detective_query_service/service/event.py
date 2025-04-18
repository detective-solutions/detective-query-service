# import standard modules
from typing import Any, Dict

subscribers: Dict[str, Any] = dict()


def subscribe(event_type: str, fn: Any) -> None:
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)


def post_event(event_type: str, data: Any) -> None:
    if event_type not in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)
