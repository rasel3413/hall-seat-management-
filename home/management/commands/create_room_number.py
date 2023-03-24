from django.core.management.base import BaseCommand
from home.models import RoomNumber

class Command(BaseCommand):
    help = 'Create RoomNumber 1 to 100'
    # py manage.py create_room_number

    def handle(self, *args, **options):
        for i in range(1, 101):
            room_number = RoomNumber(roomNo=str(i), seat='A')
            room_number.save()
            room_number = RoomNumber(roomNo=str(i), seat='B')
            room_number.save()
            room_number = RoomNumber(roomNo=str(i), seat='C')
            room_number.save()
            room_number = RoomNumber(roomNo=str(i), seat='D')
            room_number.save()
        self.stdout.write(self.style.SUCCESS('Successfully created RoomNumber 1 to 100'))
