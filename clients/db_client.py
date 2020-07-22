import boto3

from env import TABLE_NAME
import json
import decimal
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

deserializer = TypeDeserializer()
serializer = TypeSerializer()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def deserialize_db_objects(db_object):
    return {
        k: deserializer.deserialize(v) for k, v in db_object.items()
    }


def serialize_to_db_objects(data_object):
    return {
        k: serializer.serialize(v) for k, v in data_object.items()
    }


_dynamo_client = None


def _get_client():
    global _dynamo_client
    if _dynamo_client is None:
        _dynamo_client = boto3.client('dynamodb')
    return _dynamo_client


def put_connection(req_id, connection_id, user_id):
    print(req_id, "Putting in Table: {}".format(TABLE_NAME))
    _get_client().put_item(TableName=TABLE_NAME, Item=serialize_to_db_objects({
        "connection_id": connection_id,
        "user_id": user_id
    }))


def get_connections(req_id):
    print(req_id, "Getting Table: {}".format(TABLE_NAME))
    response_array = _get_client().scan(TableName=TABLE_NAME)['Items']
    return list(map(deserialize_db_objects, response_array))


def delete_connection_from_db(req_id, connection_id):
    print(req_id, "Deleting in Table: {}".format(TABLE_NAME))
    _get_client().delete_item(TableName=TABLE_NAME, Key=serialize_to_db_objects({
        "connection_id": connection_id
    }))


