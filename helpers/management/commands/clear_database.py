from django.core.management.base import BaseCommand
from ..docker_compose import ClearDatabaseTerminalCommand


class Command(BaseCommand):
    help = "Removes postgres cache created by docker-compose entirely"

    def handle(self, *args, **options):
        ClearDatabaseTerminalCommand().start()
