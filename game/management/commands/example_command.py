from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Example command'

    def handle(self, *args, **options):
        print('Example command')
