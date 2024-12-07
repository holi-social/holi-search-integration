import os

from typesense.client import Client

# thin wrapper to simplify main and testing code
class TypesenseClient(object):
    client: Client

    def __init__(self):
        self.client = Client({
            "api_key": (os.getenv("TYPESENSE_ADMIN_API_KEY")),
            "nodes": [
                {
                    "host": (os.getenv("TYPESENSE_HOST")),
                    "port": (os.getenv("TYPESENSE_PORT")),
                    "protocol": (os.getenv("TYPESENSE_PROTOCOL")),
                }
            ],
            "connection_timeout_seconds": 60 * 60,
        })

    def upsert(self, document):
        return self.client.collections[os.getenv("TYPESENSE_COLLECTION_NAME")].documents.upsert(document)

    def delete(self, id: str):
        return self.client.collections[os.getenv("TYPESENSE_COLLECTION_NAME")].documents[id].delete()