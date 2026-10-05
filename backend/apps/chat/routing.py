from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/gatherings/<int:gathering_id>/", consumers.GatheringConsumer.as_asgi()),
]
