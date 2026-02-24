import json
import logging
import threading
from kafka import KafkaConsumer

from app.config import KAFKA_BOOTSTRAP_SERVERS
from app.store.memory_store import event_store

logger = logging.getLogger(__name__)

TOPIC = "user-activity-events"
GROUP_ID = "user-activity-consumer-group"


def start_consumer():

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        enable_auto_commit=False,  # Manual commit
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest"
    )

    logger.info("Kafka Consumer started...")

    for message in consumer:
        try:
            event = message.value

            event_id = event.get("eventId")
            user_id = event.get("userId")
            event_type = event.get("eventType")

            # Log to stdout
            print(f"Received Event → eventId: {event_id}, userId: {user_id}, eventType: {event_type}")

            # Idempotency check
            if event_store.exists(event_id):
                print(f"Duplicate event detected: {event_id} — Skipping")
                consumer.commit()
                continue

            # Store event
            event_store.add(event_id, event)

            # Commit offset only after successful processing
            consumer.commit()

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Do NOT commit offset → message will retry