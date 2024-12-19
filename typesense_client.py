import os

from typesense.client import Client


class TypesenseClient(object):
    """
    Thin wrapper around the Typesense client to simplify call site and testing/mocking code.
    """

    client: Client

    def __init__(self):
        self.client = Client(
            {
                "api_key": (os.getenv("TYPESENSE_ADMIN_API_KEY")),
                "nodes": [
                    {
                        "host": (os.getenv("TYPESENSE_HOST")),
                        "port": (os.getenv("TYPESENSE_PORT")),
                        "protocol": (os.getenv("TYPESENSE_PROTOCOL")),
                    }
                ],
                "connection_timeout_seconds": 60 * 60,
            }
        )

    def upsert(self, document) -> object:
        """
        Upserts the document in Typesense

        :param document: the document to upsert
        :return: deserialized JSON document
        """
        return self.client.collections[os.getenv("TYPESENSE_COLLECTION_NAME")].documents.upsert(document)

    def delete(self, id: str) -> object:
        """
        Deletes the document from Typesense

        :param id: the id of the document to delete
        :return: deserialized JSON document
        """
        return self.client.collections[os.getenv("TYPESENSE_COLLECTION_NAME")].documents[id].delete()
