from django.urls import path, re_path
from . import views

urlpatterns = [
    path('rooms/list', views.RoomConfigListView.as_view(), name='rooms_list'),
    path(r'^(?i)(?P<room_name>[a-zA-Z0-9_-]+)/setup/', views.RoomSetupView.as_view(), name='room_setup'),
    path(r'^(?i)(?P<room_name>[a-zA-Z0-9_-]+)/start/', views.RoomStartView.as_view(), name='room-start'),
    path(r'^(?i)(?P<room_name>[a-zA-Z0-9_-]+)/gameover/<str:player_name>', views.GameOverView.as_view(), name='game-over'),
    path(r'^(?i)(?P<room_name>[a-zA-Z0-9_-]+)/result/', views.ResultView.as_view(), name='game-result'),
]
