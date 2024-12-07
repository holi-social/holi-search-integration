import functions_framework
from cloudevents.http.event import CloudEvent
from events import UserNameUpdatedEvent, get_event_type, get_event_version, UserDeletedEvent
from dataclasses import asdict

def process_user_name_updated_event(event: UserNameUpdatedEvent):
    print(f'process_user_name_updated_event: {asdict(event)}')

def process_user_deleted_event(event: UserDeletedEvent):
    print(f'process_user_deleted_event: {asdict(event)}')

def process_event(event: CloudEvent):
    type_version = (get_event_type(event), get_event_version(event))
    match type_version:
        case ('UserNameUpdated', '1.0.0'):
            return process_user_name_updated_event(UserNameUpdatedEvent(event))
        case ('UserDeleted', '1.0.0'):
            return process_user_deleted_event(UserDeletedEvent(event))

@functions_framework.cloud_event
def process_message(event: CloudEvent):
    #print(f"Received message: {event}")
    process_event(event)
