# -*- coding: utf-8 -*-

import logging
import time

import pika

logger = logging.getLogger(__name__)


class RabbitAsyncConsumer:
    """
    Helper class for an asynchronous RabbitMQ consumer.

    It takes care of all the communications aspects as well as re-connection in the event of failure. Reconnection
    attempts are done throughout the lifetime of the class instance or until an actual connection close is requested
    from the server.
    """

    def __init__(self, config, msg_callback):
        """
        :param config: The RabbitMQ server settings
        :param msg_callback: Callback function for every message received.
        """

        self.logger = logging.getLogger(__name__)

        self._protocol = 'amqp://'
        self._server = '@' + config['host']
        self._port = (':' + config['port']) or '5672'

        self._url = self._protocol
        self._url += config['user'] or ''
        self._url += (':' + config['pass']) or ''
        self._url += self._server
        self._url += self._port

        self._exchange = config['exchange']
        self._exchange_type = config['exchange_type']
        self._queue = config['queue']
        self._queue_ack = config['queue_ack']
        self._routing_key = config['topic']
        self._msg_callback = msg_callback

        self.logger.info(
            'RabbitMQ consumer for: {}{}{}{} | exchange: {} | queue: {} | topic: {}'.format(self._protocol,
                                                                                            config['user'] or '',
                                                                                            self._server,
                                                                                            self._port,
                                                                                            self._exchange,
                                                                                            self._queue,
                                                                                            self._routing_key))

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None

    #
    # Connection setup and re-establishment in the event of failure.
    #

    def connect(self):
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     self.on_connection_error,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, new_connection):
        self.logger.info('connection open')
        self._connection.add_on_close_callback(self.on_connection_closed)
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        self.logger.info('connection closed, stopping ioloop')
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._connection.add_timeout(5, self.reconnect)

    def on_connection_error(self, connection, error):
        self.logger.warning('Connection error, retrying in 5 seconds: %s', error)
        time.sleep(5)
        self.reconnect()

    def reconnect(self):
        self.logger.info('reconnecting')

        if self._connection:
            self._connection.ioloop.stop()

        if not self._closing:
            self._connection = self.connect()
            self._connection.ioloop.start()
            # the above line does not return, thats normal, its waiting for IO

    def close_connection(self):
        self._connection.close()

    #
    # Channel handling.
    #

    def open_channel(self):
        self.logger.info('opening channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.logger.info('channel open')
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_close)
        self.setup_exchange()

    def on_channel_close(self, channel, reply_code, reply_text):
        self._connection.close()

    def close_channel(self):
        self._channel.close()

    #
    # Exchange setup.
    #

    def setup_exchange(self):
        self.logger.info('setting up exchange')
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       self._exchange, self._exchange_type)

    def on_exchange_declareok(self, unused_frame):
        self.setup_queue()

    #
    # Queue handling.
    #

    def setup_queue(self):
        self.logger.info('setting up queue')
        self._channel.queue_declare(self.on_queue_declareok, self._queue, durable=True)

    def on_queue_declareok(self, frame):
        self.logger.info('binding queue')
        self._channel.queue_bind(self.on_bindok, self._queue,
                                 self._exchange, self._routing_key)

    def on_bindok(self, frame):
        self.start_consuming()

    def start_consuming(self):
        self.logger.info('starting the consuming process')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self._consumer_tag = self._channel.basic_consume(self.on_message, self._queue, no_ack=not self._queue_ack)

    def on_consumer_cancelled(self, frame):
        if self._channel:
            self._channel.close()

    def stop_consuming(self):
        if self._channel:
            self._channel.basic_cancel(self.close_channel, self._consumer_tag)

    #
    # Received message operation.
    #

    def on_message(self, unused_channel, basic_deliver, properties, body):
        self.logger.info('RabbitMQ: %r', body)

        try:
            self._msg_callback(body)
        except Exception:
            self.logger.error('Message ignored', exc_info=True)

        if self._queue_ack:
            self._channel.basic_ack(basic_deliver.delivery_tag)

    #
    # Lifecycle.
    #

    def run(self):
        self.logger.info('Starting "duracel" rabbit consumer')
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.stop()


class RabbitProducer:

    logger = logging.getLogger(__name__)

    def __init__(self, host, port, exchange):
        # TODO: Add remaining connection parameters
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=int(port)))

        self._exchange = exchange

        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=exchange,
                                       exchange_type='topic')

    def submit_message(self, message, routing_key):
        self.logger.debug(f"Submitting message to topic {routing_key} with body, {message}")
        self._channel.basic_publish(exchange=self._exchange,
                                    routing_key=routing_key,
                                    body=message)
