from dotenv import load_dotenv
import os
import requests

class ItoAPI():

    def __init__(self):
        self.__base_url = 'http://localhost:8500/api/v1'

    def _room_list(self):
        response = requests.get(
            url=f'{self.__base_url}/rooms/list'
        )
        if response.status_code == 200:
            return response.json()
        raise {'status_code': response.status_code, 'text': response.text}

    def start_game(self, room, name):
        try:
            response = self._room_list()
            rooms = {r['name'].lower(): r['name'] for r in response}
        except:
            raise "Sala não existe"

        if room.lower() in rooms.keys():
            result = requests.post(
                url=f'{self.__base_url}/{rooms[room]}/setup/',
                data={'player_name': name}
            )
            if result.status_code == 404:
                print(f'404: {rooms}')

            return {
                "success": True,
                room: rooms[room]
            }
        else:
            return {
                "success": False,
                "message": f"Sala '{room}' não existe"
            }
