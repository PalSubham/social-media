from json import dumps
from pika import BlockingConnection, ConnectionParameters
from notifications.channels import BaseNotificationChannel

# Notification broadcast channel

class NotificationBroadcastWebsocketChannel(BaseNotificationChannel):

    def _connect(self):
        connection = BlockingConnection(ConnectionParameters(host = 'localhost'))

        return connection
    
    def construct_message(self):
        return dumps(self.notification_kwargs)
    
    def notify(self, message):
        connection = self._connect()
        channel = connection.channel()

        recipient_id = str(self.notification_kwargs['recipient'])

        channel.exchange_declare(exchange = recipient_id, exchange_type = 'fanout')
        channel.basic_publish(exchange = recipient_id, routing_key = '', body = message)

        connection.close()
        return