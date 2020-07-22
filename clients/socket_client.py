import json

import boto3

from clients.db_client import delete_connection_from_db
from env import WEBSOCKET_ENDPOINT

client = None


def _get_client():
    global client
    if client is None:
        client = boto3.client('apigatewaymanagementapi', endpoint_url=WEBSOCKET_ENDPOINT)
    return client


def send_message(req_id, connection_id, message):
    try:
        _get_client().post_to_connection(
            Data=json.dumps(message),
            ConnectionId=connection_id
        )
    except client.exceptions.GoneException:
        delete_connection_from_db(req_id, connection_id)

