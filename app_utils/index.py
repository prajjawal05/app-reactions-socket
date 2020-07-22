from random import getrandbits


def parse_event_to_context(event):
    return dict(
        event_type=event["eventType"],
        connection_id=event.get("connectionId", None),
        user_id=event.get("identity", {}).get("sourceIp", ""),
        req_id=getrandbits(16)
    )
