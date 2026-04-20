export interface Poisson {
  id_poisson?: number;

  // Identité
  famille: string;
  genre: string;
  espece: string;
  nom_commun: string;

  // Écologie et Statut
  guilde_ecologique: string;
  source_guilde_ecolo: string;
  repartition_colonne_eau: string;
  source_repartition_col_eau: string;
  guilde_trophique: string;
  source_guilde_trophique: string;
  interet_halieutique: boolean | null;
  source_interet_halieutique: string;
  etat_stock: string;
  source_etat_stock: string;
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
  source_resistances: string;

  // Biologie et Morphologie
  comportement: string;
  source_comportement: string;
  periode_reproduction: string;
  forme_corps: string;
  source_forme_corps: string;
  type_peau: string;
  source_type_peau: string;

  // Capacités de nage
  locomotion: string;
  source_locomotion: string;
  endurance: string;
  source_endurance: string;
  vitesse_croisiere_juvenile_ms: number | null;
  vitesse_soutenue_juvenile_ms: number | null;
  vitesse_sprint_juvenile_ms: number | null;
  vitesse_croisiere_adulte_ms: number | null;
  vitesse_soutenue_adulte_ms: number | null;
  vitesse_sprint_adulte_ms: number | null;
  source_vitesse_nage: string;

  // Image
  aire_repartition: string | null;
}