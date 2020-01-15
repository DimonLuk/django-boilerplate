from django.core.management.base import BaseCommand
from ..docker_compose import StopServicesTerminalCommand


class Command(BaseCommand):
    help = (
        "Gracefully stops all the containers started"
        " by docker-compose (or by django commands)"
    )

    def handle(self, *args, **options):
        StopServicesTerminalCommand().start()
