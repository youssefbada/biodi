from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Dict, List, Tuple

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from core.models import Echantillonnage, Poissons


class IriPoissonServiceError(Exception):
    pass


class IriPoissonService:
    """
    Calcule IRI poissons pour un suivi (site_id, date) en 5 étapes,
    comme dans le rapport Access :

    1) 1_Ech_Totaux_Poissons
    2) 2_%_Poissons
    3) 3_IRI_Poissons
    4) 4_Total_IRI_Poissons
    5) 5_%_IRI_Poissons
    """

    # Public API

    def compute(self, site_id: str, suivi_date: date) -> Dict:
        if not site_id:
            raise IriPoissonServiceError("site_id est obligatoire.")
        if not suivi_date:
            raise IriPoissonServiceError("date est obligatoire.")

        qs = self._base_queryset(site_id, suivi_date)

        # Step 1
        totals = self._step1_totaux(qs)

        # Step 2
        by_species = self._step2_percentages(qs, totals)

        # Step 3
        iri_lines = self._step3_iri(by_species)

        # Step 4
        total_iri = self._step4_total_iri(iri_lines)

        # Step 5
        final_lines = self._step5_percent_iri(iri_lines, total_iri)

        # Output stable
        return {
            "site_id": site_id,
            "date": suivi_date,
            "total_n": float(totals["total_n"]),
            "total_p": float(totals["total_p"]),
            "total_iri": float(total_iri),
            "results": final_lines,
        }

    # Internals

    def _base_queryset(self, site_id: str, suivi_date: date):
        """
        IMPORTANT: on ne prend que les lignes où poisson_id est renseigné.
        On suppose :
        - N = nb_individus_total_pieges (ou Totaux_N dans Access)
        - P = poids_total_individus_g (ou Totaux_P)
        - O = occurrence_individus_total (ou Totaux_O) / ou présence par échantillon
        """
        return Echantillonnage.objects.filter(
            id_site=site_id, date_echantillonnage=suivi_date
        ).filter(poisson__isnull=False)

    # 1) Totaux (toutes espèces confondues)
    def _step1_totaux(self, qs) -> Dict[str, float]:
        agg = qs.aggregate(
            total_n=Coalesce(Sum("nb_individus_total_pieges"), 0),
            total_p=Coalesce(Sum("poids_total_individus_g"), 0),
            nb_echantillons=Coalesce(Count("numero"), 0),
        )

        total_n = float(agg["total_n"] or 0)
        total_p = float(agg["total_p"] or 0)
        nb_echantillons = int(agg["nb_echantillons"] or 0)

        if nb_echantillons == 0:
            raise IriPoissonServiceError(
                "Aucun échantillonnage trouvé pour ce suivi (site_id, date)."
            )

        # total_n ou total_p peuvent être 0 selon les données -> on gère plus bas
        return {
            "total_n": total_n,
            "total_p": total_p,
            "nb_echantillons": nb_echantillons,
        }

    # 2) %N, %P, %O
    def _step2_percentages(self, qs, totals: Dict[str, float]) -> List[Dict]:
        total_n = totals["total_n"]
        total_p = totals["total_p"]
        nb_echantillons = totals["nb_echantillons"]

        # Regroupement par poisson (espèce)
        grouped = qs.values("poisson_id").annotate(
            n=Coalesce(Sum("nb_individus_total_pieges"), 0),
            p=Coalesce(Sum("poids_total_individus_g"), 0),
            # occurrence brute (si déjà stockée)
            o_raw=Coalesce(Sum("occurrence_individus_total"), 0),
            # nb lignes où l'espèce apparaît (proxy occurrence Access si besoin)
            nb_presence=Count("numero"),
        )

        poisson_map = {
            p.id_poisson: p
            for p in Poissons.objects.filter(
                id_poisson__in=[g["poisson_id"] for g in grouped]
            )
        }

        result = []
        for g in grouped:
            poisson_id = g["poisson_id"]
            n = float(g["n"] or 0)
            p = float(g["p"] or 0)

            # %N et %P
            pct_n = (n / total_n * 100.0) if total_n > 0 else 0.0
            pct_p = (p / total_p * 100.0) if total_p > 0 else 0.0

            # %O : 2 stratégies (selon tes données)
            # A) Si occurrence_individus_total est bien renseigné comme "nombre d'occurrences",
            #    on peut transformer en % en normalisant par nb_echantillons.
            o_raw = float(g["o_raw"] or 0)
            if o_raw > 0:
                pct_o = (o_raw / nb_echantillons) * 100.0
            else:
                # B) Sinon on approxime comme Access: présence par échantillonnage
                pct_o = (float(g["nb_presence"]) / nb_echantillons) * 100.0

            espece_label = self._poisson_label(poisson_map.get(poisson_id))

            result.append(
                {
                    "poisson_id": poisson_id,
                    "espece": espece_label,
                    "total_n": total_n,
                    "total_p": total_p,
                    "n": n,
                    "p": p,
                    "o": pct_o,
                    "pct_n": pct_n,
                    "pct_p": pct_p,
                }
            )

        return result

    # 3) IRI = (%N + %P) * %O
    def _step3_iri(self, by_species: List[Dict]) -> List[Dict]:
        out = []
        for row in by_species:
            iri = (row["pct_n"] + row["pct_p"]) * row["o"]
            out.append({**row, "iri": float(iri)})
        return out

    # 4) Total IRI du suivi
    def _step4_total_iri(self, iri_lines: List[Dict]) -> float:
        return float(sum(r["iri"] for r in iri_lines))

    # 5) %IRI = IRI / Total_IRI * 100
    def _step5_percent_iri(self, iri_lines: List[Dict], total_iri: float) -> List[Dict]:
        out = []
        for row in iri_lines:
            pct_iri = (row["iri"] / total_iri * 100.0) if total_iri > 0 else 0.0
            out.append(
                {
                    "poisson_id": row["poisson_id"],
                    "espece": row["espece"],
                    "n": row["n"],
                    "p": row["p"],
                    "o": row["o"],
                    "pct_n": row["pct_n"],
                    "pct_p": row["pct_p"],
                    "iri": row["iri"],
                    "pct_iri": float(pct_iri),
                }
            )

        # Tri comme un ranking
        out.sort(key=lambda x: x["pct_iri"], reverse=True)
        return out

    def _poisson_label(self, poisson: Poisson | None) -> str:
        if not poisson:
            return "Poisson inconnu"
        # adapte selon ton modèle
        parts = []
        if getattr(poisson, "nom_commun", None):
            parts.append(poisson.nom_commun)
        genus = getattr(poisson, "genre", None)
        species = getattr(poisson, "espece", None)
        sci = " ".join([p for p in [genus, species] if p])
        if sci:
            parts.append(f"({sci})")
        return " ".join(parts).strip()
