from django.core.management.base import BaseCommand

from ..docker_compose import (
    RemoveDockerImage,
    RunTestsInShellTerminalCommand,
    RunTestsTerminalCommand,
)


class Command(BaseCommand):
    help = (
        "Starts postgres as well as application in testing mode\n"
        "Parameters:\n"
        "--noninteractive - by default when the container is launched you will be"
        " dropped into container shell where all the requirements are installed"
        " and environmental variables are set. By providing this flag application will"
        " be launched in background mode. Hot reloading is configured\n"
        "--rebuild - by default already built image is used. This flag starts"
        "building of new image without any cache"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--noninteractive", dest="noninteractive", action="store_true"
        )
        parser.add_argument("--rebuild", dest="rebuild", action="store_true")
        parser.set_defaults(noninteractive=False)
        parser.set_defaults(rebuild=False)

    def handle(self, *args, **options):
        if options["rebuild"]:
            RemoveDockerImage().start()
        if options["noninteractive"]:
            RunTestsTerminalCommand().start()
        else:
            RunTestsInShellTerminalCommand().start()
