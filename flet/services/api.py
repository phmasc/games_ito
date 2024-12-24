import asyncio


class ItoAPI():
    def __init__(self):
        self.rooms = {
            'Natal1': 0,
            'Natal2': 2,
            'Natal3': 3,
        }

    async def start_game(self, room, name):

        if room in self.rooms.keys():
            return {
                "success": True,
                room: self.rooms[room]
            }
