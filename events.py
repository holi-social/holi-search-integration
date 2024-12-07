import base64
import json

from cloudevents.http.event import CloudEvent
from dataclasses import dataclass

def get_event_type(cloud_event: CloudEvent) -> str:
    return cloud_event.data['message']['attributes']['eventType']

def get_event_version(cloud_event: CloudEvent) -> str:
    return cloud_event.data['message']['attributes']['eventVersion']

@dataclass
class UserPayload:
    id: str
    name: str
    email: str
    identity: str
    avatar: str

    def __init__(self, data: dict):
        self.id = data['user']['id']
        self.name = data['user']['name']
        self.email = data['user']['email']
        self.identity = data['user']['identity']
        self.avatar = data['user']['avatar']


@dataclass
class UserEvent(UserPayload):
    event_type: str
    event_version: str

    def __init__(self, cloud_event: CloudEvent):
        self.event_type = get_event_type(cloud_event)
        self.event_version = get_event_version(cloud_event)
        data = cloud_event.data['message']['data']
        super().__init__(json.loads(base64.b64decode(data)))

@dataclass
class UserNameUpdatedEvent(UserEvent):
    def __init__(self, cloud_event: CloudEvent):
        if get_event_type(cloud_event) != 'UserNameUpdated':
            raise ValueError(f'Expected event of type UserNameUpdated, got {data['eventType']}')
        super().__init__(cloud_event)

@dataclass
class UserDeletedEvent(UserEvent):
    def __init__(self, cloud_event: CloudEvent):
        if get_event_type(cloud_event) != 'UserDeleted':
            raise ValueError(f'Expected event of type UserDeleted, got {data['eventType']}')
        super().__init__(cloud_event)
