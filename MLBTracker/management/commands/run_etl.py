from django.core.management.base import BaseCommand
from MLBTracker.etl.etl_process import load_json_data, import_data


class Command(BaseCommand):
    help = "Run the ETL process to load player and statistical data"

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help="Path to JSON file")

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        try:
            self.stdout.write(self.style.SUCCESS(f"Starting ETL process for: {json_file_path}"))

            data = load_json_data(json_file_path)
            import_data(data)

            self.stdout.write(self.style.SUCCESS("ETL process completed successfully!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"ETL process failed: {e}"))
