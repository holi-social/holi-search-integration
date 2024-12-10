import os
import functions_framework
from typing import Union

from dataclasses import asdict
from cloudevents.http.event import CloudEvent

from events import UserNameUpdatedEvent, get_event_type, get_event_version, UserDeletedEvent, SpaceCreatedEvent, \
    SpaceUpdatedEvent, SpaceDeletedEvent
from typesense_client import TypesenseClient

from logging import getLogger

logger = getLogger(__name__)

def process_user_name_updated_event(client: TypesenseClient, event: UserNameUpdatedEvent):
    logger.debug(f'Processing {event}')
    document = {
        'id': f'profile_{event.user.id}',
        'type': 'profile',
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
    client.upsert(document)
    logger.info(f'Upserted user {event.user.id} in Typesense')

def process_user_deleted_event(client: TypesenseClient, event: UserDeletedEvent):
    logger.debug(f'Processing {event}')
    client.delete(f"profile_{event.user.id}")
    logger.info(f'Deleted user {event.user.id} from Typesense')

def process_space_upserting_event(client: TypesenseClient, event: Union[SpaceCreatedEvent, SpaceUpdatedEvent]):
    logger.debug(f'Processing {event}')
    document = {
        'id': f'space_{event.space.id}',
        'type': 'space',
        'title_de': event.space.name,
        'title_en': event.space.name,
        'description_de': None,  # TODO add on sending side
        'description_en': None,  # TODO add on sending side
        'location': None,
        'location_lat_lng': None,
        'image_url': event.space.avatar,
        'link_locators': {
            'space': event.space.slug
        }
    }
    client.upsert(document)
    logger.info(f'Upserted space {event.space.id} in Typesense')

def process_space_deleted_event(client: TypesenseClient, event: SpaceDeletedEvent):
    logger.debug(f'Processing {event}')
    client.delete(f"space_{event.space.id}")
    logger.info(f'Deleted space {event.space.id} in Typesense')

def process_event(client: TypesenseClient, event: CloudEvent):
    type_version = (get_event_type(event), get_event_version(event))
    match type_version:
        case ('UserNameUpdated', '1.0.0'):
            process_user_name_updated_event(client, UserNameUpdatedEvent(event))
        case ('UserDeleted', '1.0.0'):
            process_user_deleted_event(client, UserDeletedEvent(event))
        case ('UserEmailUpdated', '1.0.0'):
            # no need to process, it is sufficient to handle UserNameUpdated
            logger.debug('Ignoring UserEmailUpdated event')
            pass
        case ('SpaceCreated', '1.0.0'):
            process_space_upserting_event(client, SpaceCreatedEvent(event))
            pass
        case ('SpaceUpdated', '1.0.0'):
            process_space_upserting_event(client, SpaceUpdatedEvent(event))
            pass
        case ('SpaceDeleted', '1.0.0'):
            process_space_deleted_event(client, SpaceDeletedEvent(event))
            pass
        case (eventType, eventVersion):
            logger.debug(f'Ignoring {eventType} ({eventVersion}) event.')
            pass

@functions_framework.cloud_event
def process_message(event: CloudEvent):
    client = TypesenseClient()
    process_event(client, event)

# TODO ensure that UserUpdated or similar is emitted on updates of fields we're interested in