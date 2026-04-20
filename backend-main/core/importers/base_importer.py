from pathlib import Path
import csv
from django.db import transaction, models


class CSVImportResult:
    def __init__(self):
        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.errors = 0
        self.error_samples = []


class BaseCSVImporter:
    """
    Base importer CSV to Django Model
    - field_map: {csv_column_name: model_field_name}
    - transforms: {model_field_name: callable(raw) -> cleaned_value}
    """

    model: models.Model
    csv_filename: str
    pk_csv_column: str
    field_map: dict
    transforms: dict = {}

    def __init__(
        self,
        data_dir,
        dry_run: bool = False,
        delimiter: str = ";",
        pk_as_int: bool = True,
        encoding: str = "utf-8",
    ):
        self.data_dir = Path(data_dir)
        self.dry_run = dry_run
        self.delimiter = delimiter
        self.pk_as_int = pk_as_int
        self.encoding = encoding

    def csv_path(self) -> Path:
        return self.data_dir / self.csv_filename

    def _normalize_col(self, s: str) -> str:
        # normalise pour gérer espaces/casse
        return (s or "").replace("\ufeff", "").strip().casefold()

    def _get_pk_value(self, row: dict, result: CSVImportResult, line_no: int):
        """
        Retourne la PK nettoyée ou None si invalide (et incrémente skipped + error_samples).
        Gère colonnes bizarres en cherchant une clé équivalente.
        """
        target = self._normalize_col(self.pk_csv_column)

        # trouver la vraie clé dans row
        real_key = None
        for k in row.keys():
            if self._normalize_col(k) == target:
                real_key = k
                break

        if real_key is None:
            result.skipped += 1
            if len(result.error_samples) < 50:
                result.error_samples.append(
                    f"Ligne {line_no}: PK '{self.pk_csv_column}' introuvable. Colonnes vues={list(row.keys())}"
                )
            return None

        pk_raw = row.get(real_key)
        pk_str = str(pk_raw).strip() if pk_raw is not None else ""

        if pk_str == "":
            result.skipped += 1
            if len(result.error_samples) < 50:
                result.error_samples.append(
                    f"Ligne {line_no}: PK vide (col='{real_key}')"
                )
            return None

        if self.pk_as_int:
            try:
                return int(float(pk_str.replace(",", ".")))
            except ValueError:
                result.skipped += 1
                if len(result.error_samples) < 50:
                    result.error_samples.append(
                        f"Ligne {line_no}: PK non numérique '{pk_str}'"
                    )
                return None

        return pk_str

    def run(self) -> CSVImportResult:
        result = CSVImportResult()

        with open(self.csv_path(), "r", encoding=self.encoding, newline="") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)

            with transaction.atomic():
                for line_no, row in enumerate(reader, start=2):  # ligne 1 = header
                    try:
                        pk = self._get_pk_value(row, result, line_no)
                        if pk is None:
                            continue

                        defaults = {}
                        for csv_col, model_field in self.field_map.items():
                            raw = row.get(csv_col)
                            fn = self.transforms.get(model_field)
                            defaults[model_field] = fn(raw) if fn else raw

                        # Validation Django
                        obj = self.model(**{self.model._meta.pk.name: pk}, **defaults)
                        obj.full_clean()

                        if self.dry_run:
                            continue

                        _, created = self.model.objects.update_or_create(
                            **{self.model._meta.pk.name: pk},
                            defaults=defaults,
                        )

                        if created:
                            result.created += 1
                        else:
                            result.updated += 1

                    except Exception as e:
                        result.errors += 1
                        if len(result.error_samples) < 50:
                            result.error_samples.append(
                                f"Ligne {line_no} | PK={row.get(self.pk_csv_column)} | {e}"
                            )

                # rollback en dry-run
                if self.dry_run:
                    transaction.set_rollback(True)

        return result
