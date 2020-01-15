from django.core.management.base import BaseCommand
from ..docker_compose import ListTerminalCommand


class Command(BaseCommand):
    help = "Lists active containers"

    def handle(self, *args, **options):
        ListTerminalCommand().start()
