from .views import IndexView,room
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<str:room_name>/", room, name="room"),
]