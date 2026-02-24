import json
from kafka import KafkaProducer
from app.config import KAFKA_BOOTSTRAP_SERVERS
import logging

logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    acks="all",
    retries=5,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def publish_event(topic: str, event: dict):
    try:
        future = producer.send(topic, event)
        record_metadata = future.get(timeout=10)
        logger.info(f"Message sent to topic {record_metadata.topic}")
        return True
    except Exception as e:
        logger.error(f"Kafka publish failed: {e}")
        return False