import os
import functions_framework

from dataclasses import asdict
from cloudevents.http.event import CloudEvent

from events import UserNameUpdatedEvent, get_event_type, get_event_version, UserDeletedEvent
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
    logger.info(f'Updated user {event.user.id} in Typesense')

def process_user_deleted_event(client: TypesenseClient, event: UserDeletedEvent):
    logger.debug(f'Processing {event}')
    client.delete(f"profile_{event.user.id}")
    logger.info(f'Deleted user {event.user.id} from Typesense')

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
            # TODO implement
            logger.debug('Ignoring SpaceCreated event (yet to be implemented)')
            pass
        case ('SpaceUpdated', '1.0.0'):
            # TODO implement
            logger.debug('Ignoring SpaceCreated event (yet to be implemented)')
            pass
        case ('SpaceDeleted', '1.0.0'):
            # TODO implement
            logger.debug('Ignoring SpaceCreated event (yet to be implemented)')
            pass
        case (eventType, eventVersion):
            logger.debug(f'Ignoring {eventType} ({eventVersion}) event.')
            pass

@functions_framework.cloud_event
def process_message(event: CloudEvent):
    client = TypesenseClient()
    process_event(client, event)

# TODO ensure that UserUpdated or similar is emitted on updates of fields we're interested in