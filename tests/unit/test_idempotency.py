from app.store.memory_store import InMemoryEventStore

def test_idempotent_processing():

    store = InMemoryEventStore()

    event = {
        "eventId": "123",
        "userId": "user1",
        "eventType": "LOGIN"
    }

    # First time → should store
    assert not store.exists("123")
    store.add("123", event)

    # Second time → should detect duplicate
    assert store.exists("123")