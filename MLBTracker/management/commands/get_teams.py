from django.core.management.base import BaseCommand
from MLBTracker.etl.etl_process import import_mlb_teams, get_team_data


class Command(BaseCommand):
    help = "Run the Team Initialization process to load team data"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.SUCCESS(f"Starting Team Initialization process"))

            data = get_team_data()
            import_mlb_teams(data)

            self.stdout.write(self.style.SUCCESS(
                "Team Initialization process completed successfully!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Team Initialization process failed: {e}"))