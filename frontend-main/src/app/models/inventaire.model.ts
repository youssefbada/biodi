export interface Inventaire {
  id_inventaire?: number;

  // FK — IDs envoyés au back
  centrale_id?: number | null;
  centrale_label?: string;

  espece_poisson_id?: number | null;
  espece_poisson_label?: string;

  espece_non_poisson_id?: number | null;
  espece_non_poisson_label?: string;

  // Champs
  nom_commun: string;
  groupe_poisson: string;
  groupe_non_poisson: string;
}