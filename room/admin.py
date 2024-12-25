from django.contrib import admin
from .models import RoomConfig, Player, Room, RoomPlayer


@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_players')
    search_fields = ('name',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'victory', 'defeaut')
    search_fields = ('name',)
    list_filter = ('victory',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('get_room_config_name', 'theme', 'is_active', 'game_start_time')
    list_filter = ('is_active', 'game_start_time')
    search_fields = ('room_config__name', 'theme__name')

    def get_room_config_name(self, obj):
        return obj.room_config.name
    get_room_config_name.short_description = 'Room Config Name'


@admin.register(RoomPlayer)
class RoomPlayerAdmin(admin.ModelAdmin):
    list_display = ('get_room_name', 'get_player_name', 'card', 'ready', 'final', 'score')
    search_fields = ('room__room_config__name', 'player__name')
    list_filter = ('ready', 'final')

    def get_room_name(self, obj):
        return obj.room.room_config.name
    get_room_name.short_description = 'Room Name'

    def get_player_name(self, obj):
        return obj.player.name
    get_player_name.short_description = 'Player Name'

