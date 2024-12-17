import os
import re
import functions_framework
from typing import Union

from dataclasses import asdict
from cloudevents.http.event import CloudEvent
from typesense.exceptions import ObjectNotFound

from events import UserNameUpdatedEvent, get_event_type, get_event_version, UserDeletedEvent, SpaceCreatedEvent, \
    SpaceUpdatedEvent, SpaceDeletedEvent
from typesense_client import TypesenseClient

from logging import getLogger

logger = getLogger(__name__)

SEMVER_1XX_SERIES = r"^1\.\d+\.\d+$"

def process_user_name_updated_event(client: TypesenseClient, event: UserNameUpdatedEvent):
    logger.debug(f'Processing {event}')
    client.upsert(event.as_typesense_document())
    logger.info(f'Upserted user {event.user.id} in Typesense')

def process_user_deleted_event(client: TypesenseClient, event: UserDeletedEvent):
    logger.debug(f'Processing {event}')
    try:
        client.delete(f"profile_{event.user.id}")
    except ObjectNotFound:
        pass
    logger.info(f'Deleted user {event.user.id} from Typesense')

def process_space_upserting_event(client: TypesenseClient, event: Union[SpaceCreatedEvent, SpaceUpdatedEvent]):
    logger.debug(f'Processing {event}')
    client.upsert(event.as_typesense_document())
    logger.info(f'Upserted space {event.space.id} in Typesense')

def process_space_deleted_event(client: TypesenseClient, event: SpaceDeletedEvent):
    logger.debug(f'Processing {event}')
    try:
        client.delete(f"space_{event.space.id}")
    except ObjectNotFound:
        pass
    logger.info(f'Deleted space {event.space.id} in Typesense')

def process_event(client: TypesenseClient, event: CloudEvent):
    type_version = (get_event_type(event), re.match(SEMVER_1XX_SERIES, get_event_version(event)) is not None)
    match type_version:
        case ('UserNameUpdated', True):
            process_user_name_updated_event(client, UserNameUpdatedEvent(event))
        case ('UserDeleted', True):
            process_user_deleted_event(client, UserDeletedEvent(event))
        case ('UserEmailUpdated', True):
            # no need to process, it is sufficient to handle UserNameUpdated
            logger.debug('Ignoring UserEmailUpdated event')
            pass
        case ('SpaceCreated', True):
            process_space_upserting_event(client, SpaceCreatedEvent(event))
            pass
        case ('SpaceUpdated', True):
            process_space_upserting_event(client, SpaceUpdatedEvent(event))
            pass
        case ('SpaceDeleted', True):
            process_space_deleted_event(client, SpaceDeletedEvent(event))
            pass
        case (eventType, eventVersion):
            # UserEmailUpdated: no need to process, it is sufficient to handle UserNameUpdated because this is emitted
            # during signup and search should not display email addresses (PII)
            # All other events are assumed to (currently) not be of interest in search
            logger.debug(f'Ignoring {eventType} ({eventVersion}) event.')
            pass

@functions_framework.cloud_event
def process_message(event: CloudEvent):
    client = TypesenseClient()
    process_event(client, event)

# TODO ensure that UserUpdated or similar is emitted on updates of fields we're interested in