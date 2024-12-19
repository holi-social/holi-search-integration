import base64
import json
from dataclasses import dataclass

# noinspection PyPackageRequirements
from cloudevents.http.event import CloudEvent


def get_event_type(cloud_event: CloudEvent) -> str:
    return cloud_event.data["message"]["attributes"]["eventType"]


def get_event_version(cloud_event: CloudEvent) -> str:
    return cloud_event.data["message"]["attributes"]["eventVersion"]


def _validate_event_type(cloud_event: CloudEvent, expected_event_type: str) -> None:
    event_type = get_event_type(cloud_event)
    if event_type != expected_event_type:
        raise ValueError(f"Expected event of type {expected_event_type}, got {event_type}")


@dataclass
class UserPayload:
    id: str
    name: str
    email: str
    identity: str
    avatar: str
    about_me: str
    location: str

    def __init__(self, data: dict):
        self.id = data["user"]["id"]
        self.name = data["user"]["name"]
        self.email = data["user"]["email"]
        self.identity = data["user"]["identity"]
        self.avatar = data["user"]["avatar"]
        self.about_me = data["user"]["aboutMe"]
        self.location = data["user"]["location"]


@dataclass
class UserEvent:
    event_type: str
    event_version: str
    user: UserPayload

    def __init__(self, cloud_event: CloudEvent):
        self.event_type = get_event_type(cloud_event)
        self.event_version = get_event_version(cloud_event)
        self.user = UserPayload(json.loads(base64.b64decode(cloud_event.data["message"]["data"])))

    def __str__(self):
        return f'{type(self).__name__}(id="{self.user.id}",name="{self.user.name}",email="***",identity="{self.user.identity}",avatar="{self.user.avatar}")'


@dataclass
class UserNameUpdatedEvent(UserEvent):
    def __init__(self, cloud_event: CloudEvent):
        _validate_event_type(cloud_event, "UserNameUpdated")
        super().__init__(cloud_event)

    def as_typesense_document(self) -> object:
        return {
            "id": f"profile_{self.user.id}",
            "type": "profile",
            "title_de": self.user.name,
            "title_en": self.user.name,
            "description_de": self.user.about_me,
            "description_en": self.user.about_me,
            "location": self.user.location,
            "location_lat_lng": None,  # TODO maybe enrich?
            "image_url": self.user.avatar,
            "link_locators": {"profile": self.user.id},
        }


@dataclass
class UserDeletedEvent(UserEvent):
    def __init__(self, cloud_event: CloudEvent):
        _validate_event_type(cloud_event, "UserDeleted")
        super().__init__(cloud_event)


@dataclass
class LatLng:
    latitude: float
    longitude: float


@dataclass
class SpacePayload:
    id: str
    name: str
    slug: str
    avatar: str
    avatar_default_color: str
    description: str
    location: str
    location_lat_lng: LatLng

    def __init__(self, data: dict):
        self.id = data["space"]["id"]
        self.name = data["space"]["name"]
        self.slug = data["space"]["slug"]
        self.avatar = data["space"]["avatar"]
        self.avatar_default_color = data["space"]["avatarDefaultColor"]
        self.description = data["space"]["description"]
        self.location = data["space"]["location"]
        contains_lat_lng = (
            data["space"]["locationLatLng"] is not None
            and data["space"]["locationLatLng"]["latitude"] is not None
            and data["space"]["locationLatLng"]["longitude"] is not None
        )
        self.location_lat_lng = (
            LatLng(data["space"]["locationLatLng"].get("latitude"), data["space"]["locationLatLng"].get("longitude"))
            if contains_lat_lng
            else None
        )


@dataclass
class SpaceEvent:
    event_type: str
    event_version: str
    space: SpacePayload

    def __init__(self, cloud_event: CloudEvent):
        self.event_type = get_event_type(cloud_event)
        self.event_version = get_event_version(cloud_event)
        self.space = SpacePayload(json.loads(base64.b64decode(cloud_event.data["message"]["data"])))

    def as_typesense_document(self) -> object:
        return {
            "id": f"space_{self.space.id}",
            "type": "space",
            "title_de": self.space.name,
            "title_en": self.space.name,
            "description_de": self.space.description,
            "description_en": self.space.description,
            "location": self.space.location,
            "location_lat_lng": [self.space.location_lat_lng.latitude, self.space.location_lat_lng.longitude]
            if self.space.location_lat_lng is not None
            else None,
            "image_url": self.space.avatar,
            "link_locators": {"space": self.space.slug},
        }


@dataclass
class SpaceCreatedEvent(SpaceEvent):
    def __init__(self, cloud_event: CloudEvent):
        _validate_event_type(cloud_event, "SpaceCreated")
        super().__init__(cloud_event)


@dataclass
class SpaceUpdatedEvent(SpaceEvent):
    def __init__(self, cloud_event: CloudEvent):
        _validate_event_type(cloud_event, "SpaceUpdated")
        super().__init__(cloud_event)


@dataclass
class SpaceDeletedEvent(SpaceEvent):
    def __init__(self, cloud_event: CloudEvent):
        _validate_event_type(cloud_event, "SpaceDeleted")
        super().__init__(cloud_event)
