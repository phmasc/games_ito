from rest_framework import generics

from .models import Theme
from .serializers import ThemeSerializer

class ThemeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class ThemeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
