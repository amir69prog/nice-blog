import warnings

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache


class Command(BaseCommand):
    """ This command will clear the entire cache table """

    help = 'Clear the entire cache table'

    def add_arguments(self, parser) -> None:
        parser.add_argument('y', type=str)

    def handle(self, *args, **options):
        if options.get('y'):
            self.stdout.write(self.style.SUCCESS(
                'Clearing the entire cache...'))
            cache.clear()
            return

        action = input(self.style.NOTICE(
            'Clear the entire cache table? [yes/no]: '))
        if action.lower() == 'yes':
            self.stdout.write(self.style.SUCCESS(
                'Clearing the entire cache...'))
            cache.clear()
        elif action.lower() == 'no':
            self.stdout.write(self.style.ERROR(
                'Clearing the entire cache was canceled!'))
        else:
            self.stderr.write('Invalid action sent.')
