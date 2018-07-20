from django.core.management.base import BaseCommand
from django.db import transaction

from stats import ranking


class Command(BaseCommand):
    help = 'Test run of TrueSkills ranking'

    @transaction.atomic
    def handle(self, *args, **options):
        print('BEGIN')
        ranking.plot_rating_history()
        # ranking.calculate_trueskill_team_rating_history()
        # ranking.calculate_team_win_probability()
        print('END')