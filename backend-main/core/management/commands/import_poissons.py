from django.core.management.base import BaseCommand
from core.importers.poissons_importer import PoissonsCSVImporter


class Command(BaseCommand):
    help = "Import Poissons depuis un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--data-dir", required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        importer = PoissonsCSVImporter(
            data_dir=options["data_dir"],
            dry_run=options["dry_run"],
        )
        result = importer.run()

        self.stdout.write(
            f"Import terminé | created={result.created} "
            f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
        )

        if result.error_samples:
            self.stdout.write("Samples")
            for s in result.error_samples[:20]:
                self.stdout.write(s)
