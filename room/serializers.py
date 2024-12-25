from rest_framework import serializers
from .models import Room, Player, RoomPlayer, RoomConfig


class RoomConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomConfig
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'victory', 'defeaut']


class RoomPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = RoomPlayer
        fields = ['player', 'card', 'ready', 'final']
