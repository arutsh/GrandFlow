import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

import pika
import pika.exceptions
import pika.adapters.blocking_connection
import structlog
from typing import Optional

from app.core.config import settings
from app.services.event_handlers import handle_user_event

logger = structlog.get_logger(__name__)

_consumer_instance = None
_consumer_task = None


class EventConsumer:
    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self.exchange = settings.RABBITMQ_EXCHANGE
        self.queue = settings.RABBITMQ_QUEUE
        self._is_connected = False
        self._stop_event = asyncio.Event()

    async def init(self) -> None:
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
            self.channel = self.connection.channel()

            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type="topic",
                durable=True,
                auto_delete=False,
            )

            self.channel.queue_declare(
                queue=self.queue,
                durable=True,
                auto_delete=False,
            )

            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue,
                routing_key="user.*",
            )

            self.channel.basic_qos(prefetch_count=1)

            self._is_connected = True
            logger.info(
                "event_consumer_initialized",
                exchange=self.exchange,
                queue=self.queue,
            )
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(
                "event_consumer_connection_failed",
                error=str(e),
                rabbitmq_url=settings.RABBITMQ_URL,
            )
            self._is_connected = False
            raise

    async def close(self) -> None:
        self._stop_event.set()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self._is_connected = False
            logger.info("event_consumer_closed")

    async def start(self) -> None:
        if not self._is_connected or not self.channel:
            logger.error("consumer_not_initialized")
            raise RuntimeError("Consumer not initialized. Call init() first.")

        loop = asyncio.get_event_loop()

        def callback(ch, method, _properties, body):
            try:
                message = json.loads(body)
                event_id = message.get("event_id")
                event_type = message.get("event_type")
                payload = message.get("payload", {})

                logger.info(
                    "event_received",
                    event_id=event_id,
                    event_type=event_type,
                )

                try:
                    future = asyncio.run_coroutine_threadsafe(
                        handle_user_event(event_type, payload), loop
                    )
                    future.result()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info(
                        "event_processed",
                        event_id=event_id,
                        event_type=event_type,
                    )
                except Exception as e:
                    logger.error(
                        "event_processing_failed",
                        event_id=event_id,
                        event_type=event_type,
                        error=str(e),
                    )
                    requeue = getattr(e, "requeue", True)
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=requeue)

            except json.JSONDecodeError as e:
                logger.error("event_json_decode_failed", error=str(e))
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                logger.error("event_callback_error", error=str(e))
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback,
            auto_ack=False,
        )

        logger.info("event_consumer_started", queue=self.queue)

        def blocking_consume():
            channel = self.channel
            if channel is None:
                return
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                logger.info("event_consumer_keyboard_interrupt")
                channel.stop_consuming()
            except Exception as e:
                logger.error("event_consumer_error", error=str(e))
                raise

        executor = ThreadPoolExecutor(max_workers=1)
        await loop.run_in_executor(executor, blocking_consume)


async def init_consumer() -> EventConsumer:
    global _consumer_instance
    if _consumer_instance is None:
        _consumer_instance = EventConsumer()
        await _consumer_instance.init()
    return _consumer_instance


async def close_consumer() -> None:
    global _consumer_instance, _consumer_task
    if _consumer_instance:
        await _consumer_instance.close()
        if _consumer_task:
            _consumer_task.cancel()
            try:
                await _consumer_task
            except asyncio.CancelledError:
                pass
        _consumer_instance = None
        _consumer_task = None


async def start_consumer() -> asyncio.Task:
    global _consumer_task
    consumer = await init_consumer()
    _consumer_task = asyncio.create_task(consumer.start())
    return _consumer_task


def get_consumer() -> EventConsumer:
    global _consumer_instance  # noqa F824
    if _consumer_instance is None:
        raise RuntimeError("Consumer not initialized. Call init_consumer() first.")
    return _consumer_instance
