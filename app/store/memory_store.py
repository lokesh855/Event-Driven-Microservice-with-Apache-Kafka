from typing import Dict, List

class InMemoryEventStore:
    def __init__(self):
        self.processed_events: Dict[str, dict] = {}

    def exists(self, event_id: str) -> bool:
        return event_id in self.processed_events

    def add(self, event_id: str, event: dict):
        self.processed_events[event_id] = event

    def get_all(self) -> List[dict]:
        return list(self.processed_events.values())


event_store = InMemoryEventStore()