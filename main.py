import os
import functions_framework

from dataclasses import asdict
from cloudevents.http.event import CloudEvent

from events import UserNameUpdatedEvent, get_event_type, get_event_version, UserDeletedEvent
from typesense_client import TypesenseClient

def process_user_name_updated_event(client: TypesenseClient, event: UserNameUpdatedEvent):
    print(f'process_user_name_updated_event: {asdict(event)}')
    document = {
        'id': f'profile_{event.user.id}',
        'type': 'profile',
        'volunteering_id': event.user.id,  # TODO remove after dropping column from Typesense
        'title_de': event.user.name,
        'title_en': event.user.name,
        'description_de': None,  # TODO add on sending side
        'description_en': None,  # TODO add on sending side
        'location': None,  # TODO add on sending side
        'location_lat_lng': None,  # TODO add on sending side
        'image_url': event.user.avatar,
        'link_locators': {
            'profile': event.user.id
        }
    }
    response = client.upsert(document)
    print(f'process_user_name_updated_event: {response}')

def process_user_deleted_event(client: TypesenseClient, event: UserDeletedEvent):
    print(f'process_user_deleted_event: {asdict(event)}')
    response = client.delete(f"profile_{event.user.id}")
    print(f'process_user_deleted_event response: {response}')

def process_event(client: TypesenseClient, event: CloudEvent):
    type_version = (get_event_type(event), get_event_version(event))
    match type_version:
        case ('UserNameUpdated', '1.0.0'):
            process_user_name_updated_event(client, UserNameUpdatedEvent(event))
        case ('UserDeleted', '1.0.0'):
            process_user_deleted_event(client, UserDeletedEvent(event))

@functions_framework.cloud_event
def process_message(event: CloudEvent):
    client = TypesenseClient()
    process_event(client, event)
