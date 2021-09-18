from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import Command as RunserverCommand

from business.machine_settings import MODULES


class Command(RunserverCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--camera',
            default=False,
            action='store',
            help='Start camera',
        )
        super(Command, self).add_arguments(parser)

    def execute(self, *args, **options):
        super(Command, self).execute(self, *args, **options)

    def get_handler(self, *args, **options):
        super(Command, self).get_handler(*args, **options)

    def handle(self, *args, **options):
        if options['camera']:
            MODULES['OPEN_CAMERA'] = True
        else:
            MODULES['OPEN_CAMERA'] = False

        super(Command, self).handle(*args, **options)

    def run(self, **options):
        super(Command, self).run(**options)

    def inner_run(self, *args, **options):
        super(Command, self).inner_run(*args, **options)
