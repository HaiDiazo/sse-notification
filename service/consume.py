import pika
import asyncio
import json

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from core.base import settings


class ConsumeService:
    def __init__(self):
        self.__connection: BlockingConnection = None
        self.__channel: BlockingChannel = None

    def _credentials(self):
        return pika.PlainCredentials(
            username=settings.BROKER_USER,
            password=settings.BROKER_PASS
        )

    def _params(self):
        return pika.ConnectionParameters(
            host=settings.BROKER_HOST,
            port=settings.BROKER_PORT,
            virtual_host=settings.BROKER_VHOST,
            credentials=self._credentials()
        )

    def _open_connection(self):
        self.__connection = pika.BlockingConnection(parameters=self._params())
        self.__channel = self.__connection.channel()

    def _declare_queue(self):
        self.__channel.exchange_declare(exchange=settings.BROKER_EXCHANGE)
        self.__channel.queue_declare(queue=settings.BROKER_QUEUE)
        self.__channel.queue_bind(queue=settings.BROKER_QUEUE,
                                  routing_key=settings.BROKER_ROUTING,
                                  exchange=settings.BROKER_EXCHANGE)

    def _close_connection(self):
        self.__channel.close()
        self.__connection.close()

    def produce(self, message: dict):
        self._open_connection()
        self.__channel.basic_publish(
            exchange=settings.BROKER_EXCHANGE,
            routing_key=settings.BROKER_ROUTING,
            body=json.dumps(message).encode('utf-8')
        )
        self._close_connection()

    async def consume(self):
        self._open_connection()
        self._declare_queue()
        method_frame, properties, body = self.__channel.basic_get(settings.BROKER_QUEUE, auto_ack=False)
        if method_frame is None:
            self._close_connection()
            yield {"data": "Nothing Notification"}
        else:
            self.__channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            self._close_connection()
            data = json.loads(body.decode('utf-8'))
            yield {"data": data['error_message']}
        await asyncio.sleep(5)
