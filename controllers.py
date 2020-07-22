from clients.db_client import put_connection, delete_connection_from_db, get_connections
from clients.socket_client import send_message


def connect_socket(context, *args):
    put_connection(context['req_id'], context['connection_id'], context['user_id'])


def disconnect_socket(context, *args):
    delete_connection_from_db(context['req_id'], context['connection_id'])


def receive_message(context, body):
    print(context['req_id'], "Received Message successfully: {}".format(body))


def send_messages(context, body):
    connections = get_connections(context['req_id'])
    connection_ids = list(map(lambda conn: conn['connection_id'], connections))
    print(context['req_id'], "Active Connections: {}".format(connection_ids))
    for connection_id in connection_ids:
        send_message(context['req_id'], connection_id, body)