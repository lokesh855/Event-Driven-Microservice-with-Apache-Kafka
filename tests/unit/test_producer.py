import pytest
from unittest.mock import patch
from app.producer import publish_event

@patch("app.producer.producer")
def test_publish_event_success(mock_producer):
    mock_future = mock_producer.send.return_value
    mock_future.get.return_value = True

    result = publish_event("user-activity-events", {"key": "value"})
    assert result is True


@patch("app.producer.producer")
def test_publish_event_failure(mock_producer):
    mock_producer.send.side_effect = Exception("Kafka error")

    result = publish_event("user-activity-events", {"key": "value"})
    assert result is False