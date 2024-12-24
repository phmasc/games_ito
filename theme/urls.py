from django.urls import path
from . import views

urlpatterns = [
    path('theme/', views.ThemeListCreateAPIView.as_view(), name='theme_list'),
    path('theme/<int:pk>', views.ThemeRetrieveUpdateDestroyAPIView.as_view(), name='theme_detail'),
]
