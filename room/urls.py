from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/setup/', views.RoomSetupView.as_view(), name='room_setup'),
    path('<str:room_name>/start', views.RoomStartView.as_view(), name='room-start'),
    path('<str:room_name>/gameover/<str:player_name>', views.GameOverView.as_view(), name='game-over'),
    path('<str:room_name>/result', views.ResultView.as_view(), name='game-result'),
]
