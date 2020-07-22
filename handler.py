import json
from app_utils.index import parse_event_to_context
from controllers import *

handler_func_map = {
    "CONNECT": connect_socket,
    "DISCONNECT": disconnect_socket,
    "MESSAGE": receive_message,
    "SEND_MESSAGE": send_messages
}


def lambda_handler(event, lambda_context):
    context = parse_event_to_context(event["requestContext"])
    body = json.loads(event.get("body", "{}"))
    print("Received Body: {} Context: {}".format(body, context))
    handler_func_map[context["event_type"]](context, body)
    return {
        "statusCode": 200
    }