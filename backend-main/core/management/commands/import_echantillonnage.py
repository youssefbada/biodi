from django.core.management.base import BaseCommand
from core.importers.echantillonnage_importer import EchantillonnageCSVImporter


class Command(BaseCommand):
    help = "Import Echantillonnage depuis un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--data-dir", required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        importer = EchantillonnageCSVImporter(
            data_dir=options["data_dir"],
            dry_run=options["dry_run"],
        )
        result = importer.run()

        self.stdout.write(
            f"Import terminé | created={result.created} "
            f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
        )

        if result.errors:
            self.stdout.write(self.style.WARNING("Exemples d’erreurs:"))
            for e in result.error_samples[:20]:
                self.stdout.write(self.style.WARNING(f" - {e}"))

            self.stdout.write(
                self.style.SUCCESS(
                    f"Import terminé | created={result.created} "
                    f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
                )
            )
