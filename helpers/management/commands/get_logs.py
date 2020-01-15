from django.core.management.base import BaseCommand
from ..docker_compose import LogsTerminalCommand


class Command(BaseCommand):
    help = (
        "Populate logs from docker-compose."
        " Use it when containers are run in noninteractive mode"
    )

    def handle(self, *args, **options):
        LogsTerminalCommand().start()
