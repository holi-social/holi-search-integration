import base64

def process_message(event, context):
    """
    Cloud Function triggered by a Pub/Sub message.

    Args:
        event (dict): The event payload, which includes the message data.
        context (google.cloud.functions.Context): Metadata about the event.

    """
    # Decode the Pub/Sub message
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
        print(f"Received message: {message}")
    else:
        print("No data found in event.")

    # Log context information
    print(f"Event ID: {context.event_id}")
    print(f"Event type: {context.event_type}")
