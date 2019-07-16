import sys, uwsgi
from pika import BlockingConnection, ConnectionParameters

def application(env, start_response):
    connection = BlockingConnection(ConnectionParameters(host = 'localhost'))

    channel = connection.channel()

    exchange = env['PATH_INFO'].replace('/', '')

    channel.exchange_declare(exchange = exchange, exchange_type = 'fanout')

    result = channel.queue_declare(exclusive = True)
    queue_name = result.method.queue

    channel.queue_bind(exchange = exchange, queue = queue_name)

    # Prevents loading workers with even distribution of task.
    # Otherwise tasks will be assigned to the workers sequentially, which may load any worker.
    channel.basic_qos(prefetch_count = 1)

    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))

    def keepalive_by_pingpong():
        '''Keeps websocket connection alive (called in every 30 seconds).'''
        print('PING/PONG...\n')

        try:
            uwsgi.websocket_recv_nb()
            connection.add_timeout(30, keepalive_by_pingpong)
        except OSError as error:
            connection.close()
            print(error)
            sys.exit(1) # The process is closed and uwsgi respawns it.
        
        return
    
    keepalive_by_pingpong()

    while True:
        for method, properties, body in channel.consume(queue_name):
            try:
                uwsgi.websocket_send(body)
            except OSError as error:
                print(error)
                sys.exit(1)
            else:
                channel.basic_ack(delivery_tag = method.delivery_tag)
    
    return