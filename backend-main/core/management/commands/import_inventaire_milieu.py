from django.core.management.base import BaseCommand
from core.importers.inventaire_milieu_importer import InventaireMilieuCSVImporter


class Command(BaseCommand):
    help = "Import InventaireMilieu depuis un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--data-dir", required=True)
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--delimiter", default=";")
        parser.add_argument("--encoding", default="utf-8")

    def handle(self, *args, **options):
        importer = InventaireMilieuCSVImporter(
            data_dir=options["data_dir"],
            dry_run=options["dry_run"],
            delimiter=options["delimiter"],
            encoding=options["encoding"],
        )
        result = importer.run()

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé | created={result.created} "
                f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
            )
        )

        if result.errors:
            self.stdout.write(self.style.WARNING("Exemples d’erreurs:"))
            for err in result.error_samples:
                self.stdout.write(f" - {err}")
