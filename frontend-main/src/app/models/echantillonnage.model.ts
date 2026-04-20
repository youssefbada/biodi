export interface Echantillonnage {
  id_echantillonnage?: number;

  // Données d'échantillonnage
  centrale_id: number | null;
  centrale_label?: string; // pour affichage
  date_echantillonnage: string;
  nombre_echantillonnage: number | null;
  duree_echantillonnage_min: number | null;
  debris_vegetaux: boolean | null;

  // Espèce piégée
  groupe: string;
  poisson_id: number | null;
  poisson_label?: string; // pour affichage
  non_poisson_id: number | null;
  non_poisson_label?: string; // pour affichage
  frequence_occurrence: string;

  // Juvéniles
  juveniles_nombre_individus: number | null;
  juveniles_pois: number | null;
  juveniles_poids_moyen: number | null;
  juveniles_occurence: number | null;
  juveniles_pct_o: number | null;
  juveniles_taille_moy_cm: number | null;
  juveniles_taux_survie: number | null;
  juveniles_taux_mortalite: number | null;

  // Adultes
  adultes_nombre_individus: number | null;
  adultes_poids: number | null;
  adultes_poids_moyen: number | null;
  adultes_occurence: number | null;
  adultes_pct_o: number | null;
  adultes_taille_moy_cm: number | null;
  adultes_taux_survie: number | null;
  adultes_taux_mortalite: number | null;

  // Totaux
  totaux_nombre_individus: number | null;
  totaux_poids: number | null;
  totaux_poids_moyen: number | null;
  totaux_occurence: number | null;
  totaux_pct_o: number | null;
  totaux_taille_moy: number | null;
  totaux_taux_survie: number | null;
  totaux_taux_mortalite: number | null;

  // Saison Hiver
  hiver_nombre_individus: number | null;
  hiver_poids: number | null;
  hiver_poids_moyen: number | null;
  hiver_occurence: number | null;
  hiver_pct_o: number | null;
  hiver_taille_moy: number | null;
  hiver_taux_survie: number | null;
  hiver_taux_mortalite: number | null;
  hiver_nombre_echantillonnage: string;

  // Saison Printemps
  printemps_nombre_individus: number | null;
  printemps_poids: number | null;
  printemps_poids_moyen: number | null;
  printemps_occurence: number | null;
  printemps_pct_o: number | null;
  printemps_taille_moy: number | null;
  printemps_taux_survie: number | null;
  printemps_taux_mortalite: number | null;
  printemps_nombre_echantillonnage: string;

  // Saison Été
  ete_nombre_individus: number | null;
  ete_poids: number | null;
  ete_poids_moyen: number | null;
  ete_occurence: number | null;
  ete_pct_o: number | null;
  ete_taille_moy: number | null;
  ete_taux_survie: number | null;
  ete_taux_mortalite: number | null;
  ete_nombre_echantillonnage: string;

  // Saison Automne
  automne_nombre_individus: number | null;
  automne_poids: number | null;
  automne_poids_moyen: number | null;
  automne_occurence: number | null;
  automne_pct_o: number | null;
  automne_taille_moy: number | null;
  automne_taux_survie: number | null;
  automne_taux_mortalite: number | null;
  automne_nombre_echantillonnage: string;

  sources: string;
}