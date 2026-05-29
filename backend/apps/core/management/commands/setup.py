from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


FIXTURES = [
    "users",
    "customers",
    "sellers",
    "products",
    "sales",
]


class Command(BaseCommand):
    help = "Flush the database and load initial fixtures (development only)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            dest="yes",
            help="Skip the confirmation prompt.",
        )

    def _confirm(self):
        self.stdout.write(
            self.style.WARNING(
                "WARNING: This will DELETE ALL DATA in the database and reload fixtures."
            )
        )
        answer = input('Type "yes" to continue, or anything else to cancel: ')
        if answer.strip().lower() != "yes":
            raise CommandError("Operation cancelled.")

    def _flush_database(self):
        try:
            call_command("flush", "--no-input")
            self.stdout.write(self.style.WARNING("Database flushed."))
        except Exception as exc:
            raise CommandError(f"Failed to flush database: {exc}") from exc

    def _load_initial_fixtures(self):
        for fixture_name in FIXTURES:
            try:
                call_command("loaddata", fixture_name)
                self.stdout.write(self.style.SUCCESS(f"Fixture loaded: {fixture_name}"))
            except Exception as exc:
                raise CommandError(
                    f'Failed to load fixture "{fixture_name}": {exc}'
                ) from exc

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            raise CommandError("This command is not allowed outside of DEBUG mode.")

        if not kwargs.get("yes"):
            self._confirm()

        self._flush_database()
        self._load_initial_fixtures()
