from cloudevents.http.event import CloudEvent

from main import process_message

attributes = {
    'id': '12833783708309476',
    'time': '2024-12-07T16:21:48.022Z',
    'specversion': '1.0',
    'datacontenttype': 'application/json',
    'type': 'google.cloud.pubsub.topic.v1.messagePublished',
    'source': '//pubsub.googleapis.com/'
}
data = {
    'message': {
        '@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
        'data': 'eyJ1c2VyIjogeyJpZCI6ICIxNDlhM2QyOS1hMGRhLTRmNTItOGUxYy02NjAzNzZiNzA4NGIiLCAibmFtZSI6ICJEYW5pZWwgaG9saSB0ZWFtIiwgImVtYWlsIjogImRhbmllbEBob2xpLnRlYW0iLCAiaWRlbnRpdHkiOiAiZGFuaWVsaG9saS50ZWFtIiwgImF2YXRhciI6ICJodHRwczovL2lrLmltYWdla2l0LmlvL2hvbGkvX0RFVl8vYXZhdGFyLzE0OWEzZDI5LWEwZGEtNGY1Mi04ZTFjLTY2MDM3NmI3MDg0Yl95djMxVVc3bEQwLmpwZyJ9fQ==',
        'attributes': {
            'eventType': 'UserNameUpdated',
            'eventVersion': '1.0.0'
        },
        'messageId': '12833783708309476',
        'publishTime': '2024-12-07T16:21:48.022Z'
    }
}

def test_process_message():
    process_message(CloudEvent(attributes, data))


if __name__ == '__main__':
    test_process_message()