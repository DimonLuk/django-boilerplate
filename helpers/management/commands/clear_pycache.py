from django.core.management.base import BaseCommand
from ..docker_compose import RemovePycacheTerminalCommand


class Command(BaseCommand):
    help = "Removes __pycache__ folders all over the project"

    def handle(self, *args, **options):
        RemovePycacheTerminalCommand().start()
