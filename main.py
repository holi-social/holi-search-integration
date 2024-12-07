import base64
import json

import functions_framework
from cloudevents.http.event import CloudEvent
from dataclasses import dataclass

@dataclass
class UserPayload:
    id: str
    name: str
    email: str
    identity: str
    avatar: str

    def __init__(self, data: dict):
        print(f"UserPayload: {data}")
        self.id = data['user']['id']
        self.name = data['user']['name']
        self.email = data['user']['email']
        self.identity = data['user']['identity']
        self.avatar = data['user']['avatar']


@dataclass
class UserNameUpdatedEvent(UserPayload):
    event_type: str
    event_version: str

    def __init__(self, event: CloudEvent):
        message = event['data']['message']
        if message['attributes']['eventType'] != 'UserNameUpdated':
            raise ValueError(f'Expected event of type UserNameUpdated, got {data['eventType']}')
        self.event_type = message['attributes']['eventType']
        self.event_version = message['attributes']['eventVersion']
        super().__init__(json.loads(decode_message_data(message['data'])))


def process_user_name_updated_event(event: UserNameUpdatedEvent):
    print(f'process_user_name_updated_event: {event}')

def decode_message_data(data: str):
    return base64.b64decode(data)

def process_event(event: CloudEvent):
    attributes = event['data']['message']['attributes']
    if attributes['eventType'] == 'UserNameUpdated' and attributes['eventVersion'] == '1.0.0': # TODO backwards semver
        process_user_name_updated_event(UserNameUpdatedEvent(event))

@functions_framework.cloud_event
def process_message(cloud_event: CloudEvent):
    print(f"Received message: {cloud_event}")
    process_event(cloud_event)
