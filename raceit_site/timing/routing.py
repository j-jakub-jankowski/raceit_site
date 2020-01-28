from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/live_display', consumers.LiveDisplayConsumer),
]
