// ─── Types ───
export type MilieuType = 'Marin' | 'Fleuve' | 'Estuaire';
export type TypeCircuit = 'Ouvert' | 'Fermé';
export type TypeFiltration = 'Tambour' | 'Bande' | 'Grille';
export type PressionNettoyage = 'Haute' | 'Basse';
export type TypeTraitementChimique = 'ELECTROCHLORATION' | 'CHLORE' | 'AUTRE';
export type FonctionnementFiltre = 'Continu' | 'Intermittent';
export type PriseDeauRejetEau = 'Amont' | 'Aval' | 'Lateral';

// ─── Options selects ───
export const MILIEU_TYPE_OPTIONS: { value: MilieuType | ''; label: string }[] = [
  { value: '', label: 'Tous' },
  { value: 'Marin', label: 'Marin' },
  { value: 'Fleuve', label: 'Fleuve' },
  { value: 'Estuaire', label: 'Estuaire' }
];

export const TYPE_CIRCUIT_OPTIONS: { value: TypeCircuit | ''; label: string }[] = [
  { value: '', label: 'Tous les types' },
  { value: 'Ouvert', label: 'Ouvert' },
  { value: 'Fermé', label: 'Fermé' },
];

export const TYPE_FILTRATION_OPTIONS: { value: TypeFiltration | ''; label: string }[] = [
  { value: '', label: 'Tous' },
  { value: 'Tambour', label: 'Tambour' },
  { value: 'Bande', label: 'Bande' },
  { value: 'Grille', label: 'Grille' },
];

export const PRESSION_NETTOYAGE_OPTIONS: { value: PressionNettoyage | ''; label: string }[] = [
  { value: '', label: 'Tous' },
  { value: 'Haute', label: 'Haute pression' },
  { value: 'Basse', label: 'Basse pression' },
];

export const TYPE_TRAITEMENT_CHIMIQUE_OPTIONS: { value: TypeTraitementChimique; label: string }[] = [
  { value: 'ELECTROCHLORATION', label: 'Électrochloration' },
  { value: 'CHLORE', label: 'Chlore' },
  { value: 'AUTRE', label: 'Autre' },
];

export const FONCTIONNEMENT_FILTRE_OPTIONS: { value: FonctionnementFiltre | ''; label: string }[] = [
  { value: '', label: 'Tous' },
  { value: 'Continu', label: 'Continu' },
  { value: 'Intermittent', label: 'Intermittent' },
];

export const LOCALISATION_OPTIONS: { value: PriseDeauRejetEau | ''; label: string }[] = [
  { value: '', label: 'Sélectionner' },
  { value: 'Amont', label: 'Amont' },
  { value: 'Aval', label: 'Aval' },
  { value: 'Lateral', label: 'Latéral' },
];

export const CANAL_AMENEE_OPTIONS = [
  { value: 'tous', label: 'Tous' },
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
];

export const MILIEU_BADGE_COLORS: Record<string, string> = {
  Marin: 'badge-blue',
  Fleuve: 'badge-green',
  Estuaire: 'badge-teal',
};