import requests
import time

BASE_URL = "http://localhost:8000"

def test_end_to_end_flow():

    payload1 = {
        "userId": "user1",
        "eventType": "LOGIN",
        "payload": {}
    }

    payload2 = {
        "userId": "user1",
        "eventType": "LOGIN",
        "payload": {}
    }

    # Send duplicate events
    r1 = requests.post(f"{BASE_URL}/events/generate", json=payload1)
    r2 = requests.post(f"{BASE_URL}/events/generate", json=payload2)

    assert r1.status_code == 201
    assert r2.status_code == 201

    # Wait for consumer processing
    time.sleep(3)

    response = requests.get(f"{BASE_URL}/events/processed")
    assert response.status_code == 200

    events = response.json()

    # Ensure unique events only
    event_ids = [event["eventId"] for event in events]
    assert len(event_ids) == len(set(event_ids))