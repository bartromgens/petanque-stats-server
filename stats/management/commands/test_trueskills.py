from django.core.management.base import BaseCommand
from django.db import transaction

from stats import ranking


class Command(BaseCommand):
    help = 'Test run of TrueSkills ranking'

    @transaction.atomic
    def handle(self, *args, **options):
        print('BEGIN')
        ranking.calculate_trueskill_rating_history()
        print('END')