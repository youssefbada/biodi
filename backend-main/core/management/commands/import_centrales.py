from django.core.management.base import BaseCommand
from core.importers.centrales_importer import CentralesCSVImporter


class Command(BaseCommand):
    help = "Import Centrales depuis un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--data-dir", required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        importer = CentralesCSVImporter(
            data_dir=options["data_dir"], dry_run=options["dry_run"]
        )
        result = importer.run()

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé | created={result.created} "
                f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
            )
        )

        if result.errors:
            self.stdout.write(self.style.WARNING("ERREURS"))
            for msg in result.error_samples:
                self.stdout.write(self.style.WARNING(msg))
