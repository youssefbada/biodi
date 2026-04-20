from __future__ import annotations

from core.importers.base_importer import BaseCSVImporter
from core.importers.cleaners import strip_or_none, strip_or_empty, normalize_enum
from core.enums.echantillonnage_enum import GroupeEnum
from core.models import InventaireMilieu, Centrales, Poissons, NonPoissons


class InventaireMilieuCSVImporter(BaseCSVImporter):
    """
    CSV attendu:
     - Site
     - Espèce
     - Nom_commun
     - Groupe
     - Numero_inventaire

    Comportement PK:
     - si Numero_inventaire est présent et non vide -> update_or_create
     - sinon -> create()
    """

    model = InventaireMilieu
    csv_filename = "Inventaire.csv"
    pk_csv_column = "N°"

    # CSV_COL -> model_field
    field_map = {
        "Site": "centrale",
        "Espèce": "espece_any",
        "Nom_commun": "nom_commun",
        "Groupe": "groupe_any",
    }

    @staticmethod
    def _resolve_centrale(site_raw: str | None) -> Centrales | None:
        site = strip_or_none(site_raw)
        if not site:
            return None

        site = site.strip()
        # 1) code_nom
        obj = Centrales.objects.filter(code_nom__iexact=site).first()
        if obj:
            return obj

        # 2) fallback sur site_name
        obj = Centrales.objects.filter(site_name__iexact=site).first()
        return obj

    @staticmethod
    def _resolve_species(
        espece_raw: str | None,
    ) -> tuple[Poissons | None, NonPoissons | None]:
        espece = strip_or_none(espece_raw)
        if not espece:
            return None, None

        espece = espece.strip()

        # 1) match exact sur "espece"
        p = Poissons.objects.filter(espece__iexact=espece).first()
        if p:
            return p, None

        np = NonPoissons.objects.filter(espece__iexact=espece).first()
        if np:
            return None, np

        # 2) fallback sur nom_commun
        p = Poissons.objects.filter(nom_commun__iexact=espece).first()
        if p:
            return p, None

        np = NonPoissons.objects.filter(nom_commun__iexact=espece).first()
        if np:
            return None, np

        return None, None

    def run(self):
        """
        On override run() pour supporter l'absence de Numero_inventaire
        """
        from core.importers.base_importer import CSVImportResult
        import csv
        from django.db import transaction

        result = CSVImportResult()

        with open(self.csv_path(), "r", encoding=self.encoding, newline="") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)

            with transaction.atomic():
                for line_no, row in enumerate(reader, start=2):
                    try:
                        # ---- resolve centrale ----
                        centrale = self._resolve_centrale(row.get("Site"))
                        if centrale is None:
                            result.errors += 1
                            if len(result.error_samples) < 50:
                                result.error_samples.append(
                                    f"Ligne {line_no} | Site={row.get('Site')} | Centrale introuvable (match code_nom/site_name)"
                                )
                            continue

                        # ---- resolve espèce (Poisson / NonPoisson) ----
                        poisson, non_poisson = self._resolve_species(row.get("Espèce"))
                        if poisson:
                            print(
                                f"[MATCH POISSON] Ligne {line_no} -> Espèce='{row.get('Espèce')}' -> ID={poisson.id_poisson}"
                            )

                        if non_poisson:
                            print(
                                f"[MATCH NON POISSON] Ligne {line_no} -> Espèce='{row.get('Espèce')}' -> ID={non_poisson.id_non_poisson}"
                            )

                        if poisson is None and non_poisson is None:
                            result.errors += 1
                            if len(result.error_samples) < 50:
                                result.error_samples.append(
                                    f"Ligne {line_no} | Espèce={row.get('Espèce')} | Espèce introuvable (Poissons/NonPoissons)"
                                )
                            continue

                        # ---- groupe (colonne unique) -> selon espèce ----
                        groupe_raw = row.get("Groupe")
                        if strip_or_none(groupe_raw):
                            groupe_value = normalize_enum(groupe_raw, GroupeEnum)

                            if poisson:
                                print(
                                    f"[GROUPE POISSON] Ligne {line_no} -> {groupe_value}"
                                )

                            if non_poisson:
                                print(
                                    f"[GROUPE NON POISSON] Ligne {line_no} -> {groupe_value}"
                                )
                        else:
                            groupe_value = ""
                        groupe_poisson = groupe_value if poisson else ""
                        groupe_non_poisson = groupe_value if non_poisson else ""

                        defaults = {
                            "centrale": centrale,
                            "espece_poisson": poisson,
                            "espece_non_poisson": non_poisson,
                            "nom_commun": strip_or_empty(row.get("Nom_commun")),
                            "groupe_poisson": groupe_poisson,
                            "groupe_non_poisson": groupe_non_poisson,
                        }

                        # validation Django
                        obj = self.model(**defaults)
                        obj.full_clean()

                        if self.dry_run:
                            continue

                        pk = self._get_pk_value(row, result, line_no)  # renvoie none
                        if pk is None:
                            # pas de pk -> create (id auto)
                            self.model.objects.create(**defaults)
                            result.created += 1
                        else:
                            # pk -> update_or_create
                            _, created = self.model.objects.update_or_create(
                                **{self.model._meta.pk.name: pk}, defaults=defaults
                            )
                            result.created += 1 if created else 0
                            result.updated += 0 if created else 1

                    except Exception as e:
                        result.errors += 1
                        if len(result.error_samples) < 50:
                            result.error_samples.append(f"Ligne {line_no} | {e}")

                if self.dry_run:
                    transaction.set_rollback(True)

        return result
