import base64
import functions_framework

@functions_framework.cloud_event
def process_message(cloud_event):
    # TODO remove inspection prints
    print(f"Received message: {cloud_event}")
    if 'data' in cloud_event:
        message = base64.b64decode(event['data']).decode('utf-8')
        print(f"Received message: {message}")
    else:
        print("No data found in event.")
