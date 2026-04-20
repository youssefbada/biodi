import {
  MilieuType,
  TypeCircuit,
  TypeFiltration,
  PressionNettoyage,
  TypeTraitementChimique,
  FonctionnementFiltre,
  PriseDeauRejetEau,
} from '../core/constants/centrale.constants';

export interface Centrale {
  // Identité / Site (Tableau 1.a)
  id?: number;
  site_name: string;
  code_nom: string;
  milieu_type: MilieuType | '';
  source_froide: string;

  // Caractéristiques CNPE (Tableau 1.b)
  nbre_reacteurs: number | null;
  puissance_reacteurs_mwe: number | null;
  debit_aspire_par_tranche_m3s: number | null;
  debit_total_aspire_m3s: number | null;
  taux_disponibilite_moyen_tranches: string;

  // Circuit / Filtration (Tableau 1.c)
  type_circuit: TypeCircuit | '';
  type_filtration: TypeFiltration | '';
  dimension_filtre_h_l_m: string;
  maillage_mm: number | null;
  pression_nettoyage: PressionNettoyage | '';
  traitement_chimique: boolean | null;
  type_traitement_chimique: TypeTraitementChimique | '';
  circuits_crf_sec_separes: boolean | null;
  pompes_separees: boolean | null;
  fonctionnement_filtre: FonctionnementFiltre | '';
  temps_moyen_emersion_min: number | null;
  systeme_recuperation: boolean | null;
  presence_goulotte: boolean | null;
  goulotte_hauteur_eau: number | null;
  presence_pre_grille: boolean | null;
  espacement_pre_grille_mm: number | null;

  // Prise d'eau / Rejet (Tableau 1.d)
  presence_canal_amenee: boolean | null;
  localisation_prise_eau: PriseDeauRejetEau | '';
  localisation_rejet_eau: PriseDeauRejetEau | '';
  profondeur_rejet_eau_m: number | null;
  distance_cote_rejet_eau_m: number | null;
  volume_eau_rejetee_m3s: number | null;
  temperature_rejet_c: number | null;
  temperature_milieu_c: number | null;
  delta_t_c: number | null;
}

export type CentraleListResponse = Centrale[];

export interface CentraleFilters {
  search?: string;
  milieu_type?: string;
  type_circuit?: string;
  presence_canal_amenee?: boolean | null;
  page?: number;
  page_size?: number;
}