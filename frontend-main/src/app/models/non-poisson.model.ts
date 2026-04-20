export interface NonPoisson {
  id_non_poisson?: number;

  // Groupe + Identité
  groupe: string;
  famille: string;
  genre: string;
  espece: string;
  nom_commun: string;

  // Écologie
  guilde_ecologique: string;
  source_guilde_ecolo: string;
  repartition_colonne_eau: string;
  source_repartition_col_eau: string;
  guilde_trophique: string;
  source_guilde_trophique: string;
  enjeu_halieutique: boolean | null;
  source_enjeu_halieutique: string;
  etat_stock: string;
  source_stock: string;
  statut_protection: string;
  source_protection: string;
  conservation_fr: string;
  conservation_eu: string;
  conservation_md: string;
  source_conservation: string;

  // Sensibilités
  sensibilite_lumiere: string;
  source_sens_lumiere: string;
  sensibilite_courants_eau: string;
  source_sens_courant: string;
  sensibilite_sonore: string;
  source_sens_sonore: string;

  // Résistances
  resistance_chocs_mecaniques: string;
  resistance_chocs_chimiques: string;
  resistance_chocs_thermiques: string;
  source_resistance_chocs: string;

  // Nage
  endurance: string;
  source_endurance: string;
  vitesse_nage_min_ms: number | null;
  vitesse_nage_moy_ms: number | null;
  vitesse_nage_max_ms: number | null;
  source_vitesse_nage: string;

  // Image
  aire_repartition: string | null;
}