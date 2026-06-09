import json
import uuid
from datetime import datetime
from typing import Dict, Any

import pika
import pika.exceptions
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

_publisher_instance = None


class EventPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = settings.RABBITMQ_EXCHANGE
        self._is_connected = False

    async def init(self) -> None:
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            self.channel = self.connection.channel()

            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type="topic",
                durable=True,
                auto_delete=False,
            )

            self._is_connected = True
            logger.info("event_publisher_initialized", exchange=self.exchange)
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(
                "event_publisher_connection_failed",
                error=str(e),
                rabbitmq_url=settings.RABBITMQ_URL,
            )
            self._is_connected = False
            raise

    async def close(self) -> None:
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self._is_connected = False
            logger.info("event_publisher_closed")

    async def publish(
        self, event_type: str, payload: Dict[str, Any]
    ) -> None:
        if not self._is_connected or not self.channel:
            logger.warning(
                "publish_attempted_without_connection",
                event_type=event_type,
            )
            return

        try:
            event_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat() + "Z"

            event_body = {
                "event_id": event_id,
                "timestamp": timestamp,
                "event_type": event_type,
                "payload": payload,
            }

            message = json.dumps(event_body)

            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=event_type,
                body=message,
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                ),
            )

            logger.info(
                "event_published",
                event_id=event_id,
                event_type=event_type,
                exchange=self.exchange,
            )
        except Exception as e:
            logger.error(
                "event_publish_failed",
                event_type=event_type,
                error=str(e),
            )
            raise


async def init_publisher() -> EventPublisher:
    global _publisher_instance
    if _publisher_instance is None:
        _publisher_instance = EventPublisher()
        await _publisher_instance.init()
    return _publisher_instance


async def close_publisher() -> None:
    global _publisher_instance
    if _publisher_instance:
        await _publisher_instance.close()
        _publisher_instance = None


def get_publisher() -> EventPublisher:
    global _publisher_instance
    if _publisher_instance is None:
        raise RuntimeError("Publisher not initialized. Call init_publisher() first.")
    return _publisher_instance
