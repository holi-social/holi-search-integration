import base64
import json

from unittest.mock import patch

from cloudevents.http import CloudEvent
from cloudevents.http.event import CloudEvent
from main import process_event

attributes = {
    'id': '12833783708309476',
    'time': '2024-12-07T16:21:48.022Z',
    'specversion': '1.0',
    'datacontenttype': 'application/json',
    'type': 'google.cloud.pubsub.topic.v1.messagePublished',
    'source': '//pubsub.googleapis.com/'
}

user_payload = {
    'id': '149a3d29-a0da-4f52-8e1c-660376b7084b',
    'name': 'Daniel holi team',
    'email': 'daniel@holi.team',
    'identity': 'danielholi.team',
    'avatar': 'https://ik.imagekit.io/holi/_DEV_/avatar/149a3d29-a0da-4f52-8e1c-660376b7084b_yv31UW7lD0.jpg',
}

def message_data(event_type, event_version, data):
    return {
        'message': {
            '@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
            'data': base64.b64encode(json.dumps(data).encode('utf-8')),
            'attributes': {
                'eventType': event_type,
                'eventVersion': event_version,
            },
            'messageId': '12833783708309476',
            'publishTime': '2024-12-07T16:21:48.022Z'
        }
}

@patch('typesense.client.Client')
def test_user_name_updated(mock_client):
    process_event(mock_client, CloudEvent(attributes, message_data('UserNameUpdated', '1.0.0', {'user': user_payload})))
    mock_client.upsert.assert_called_with({
        'id': f'profile_{user_payload["id"]}',
        'type': 'profile',
        'title_de': user_payload['name'],
        'title_en': user_payload['name'],
        'description_de': None,  # TODO add on sending side
        'description_en': None,  # TODO add on sending side
        'location': None,  # TODO add on sending side
        'location_lat_lng': None,  # TODO add on sending side
        'image_url': user_payload['avatar'],
        'link_locators': {
            'profile': user_payload['id'],
        }
    })

@patch('typesense.client.Client')
def test_user_deleted(mock_client):
    process_event(mock_client, CloudEvent(attributes, message_data('UserDeleted', '1.0.0', {'user': user_payload})))
    mock_client.delete.assert_called_with(f"profile_{user_payload['id']}")

if __name__ == '__main__':
    process_event()