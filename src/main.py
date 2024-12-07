def process_message(event, context):
    """
    Entry point for the Pub/Sub-triggered Cloud Function.
    :param event: Pub/Sub event payload
    :param context: Metadata about the event
    """
    print(f"Received event: {event['data']} with context: {context}")
