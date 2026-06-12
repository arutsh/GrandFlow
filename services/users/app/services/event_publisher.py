import json
import uuid
from datetime import datetime
from typing import Dict, Any

import aio_pika
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

_publisher_instance = None


class EventPublisher:
    def __init__(self):
        self.connection: aio_pika.abc.AbstractConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None
        self._is_connected = False

    async def init(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()

            self.exchange = await self.channel.declare_exchange(
                settings.RABBITMQ_EXCHANGE,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
                auto_delete=False,
            )

            self._is_connected = True
            logger.info("event_publisher_initialized", exchange=settings.RABBITMQ_EXCHANGE)
        except Exception as e:
            logger.error(
                "event_publisher_connection_failed",
                error=str(e),
                rabbitmq_url=settings.RABBITMQ_URL,
            )
            self._is_connected = False
            raise

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            self._is_connected = False
            logger.info("event_publisher_closed")

    async def publish(
        self, event_type: str, payload: Dict[str, Any]
    ) -> None:
        if not self._is_connected or not self.channel or not self.exchange:
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

            message = aio_pika.Message(
                body=json.dumps(event_body).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            await self.exchange.publish(message, routing_key=event_type)

            logger.info(
                "event_published",
                event_id=event_id,
                event_type=event_type,
                exchange=settings.RABBITMQ_EXCHANGE,
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
