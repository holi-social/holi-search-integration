import base64
import functions_framework

@functions_framework.cloud_event
def process_message(cloud_event):
    print(f"Received message: {cloud_event}")
