// ─── Types ───
export type MilieuType = 'Marin' | 'Fleuve' | 'Estuaire';
export type TypeCircuit = 'Ouvert' | 'Fermé';
export type TypeFiltration = 'Filtre à chaîne' | 'Tambour filtrant';
export type PressionNettoyage = 'Haute pression' | 'Basse pression' | 'MOYENNE_PRESSION';
export type TypeTraitementChimique = 'Electrochloration' | 'Monochloration';
export type FonctionnementFiltre = 'En continu' | 'Séquentiel';
export type PriseDeauRejetEau = "Canal d'amené" | 'Large';

// ─── Options selects ───
export const MILIEU_TYPE_OPTIONS: { value: MilieuType | ''; label: string }[] = [
  { value: '', label: 'Tous' },
  { value: 'Marin', label: 'Marin' },
  { value: 'Fleuve', label: 'Fleuve' },
  { value: 'Estuaire', label: 'Estuaire' },
];

export const TYPE_CIRCUIT_OPTIONS: { value: TypeCircuit | ''; label: string }[] = [
  { value: '', label: 'Tous les types' },
  { value: 'Ouvert', label: 'Ouvert' },
  { value: 'Fermé', label: 'Fermé' },
];

export const TYPE_FILTRATION_OPTIONS: { value: TypeFiltration | ''; label: string }[] = [
  { value: '', label: 'Sélectionner' },
  { value: 'Filtre à chaîne', label: 'Filtre à chaîne' },
  { value: 'Tambour filtrant', label: 'Tambour filtrant' },
];

export const PRESSION_NETTOYAGE_OPTIONS: { value: PressionNettoyage | ''; label: string }[] = [
  { value: '', label: 'Sélectionner' },
  { value: 'Basse pression', label: 'Basse pression' },
  { value: 'Haute pression', label: 'Haute pression' },
  { value: 'MOYENNE_PRESSION', label: 'Moyenne pression' },
];

export const TYPE_TRAITEMENT_CHIMIQUE_OPTIONS: { value: TypeTraitementChimique; label: string }[] = [
  { value: 'Electrochloration', label: 'Électrochloration' },
  { value: 'Monochloration', label: 'Monochloration' },
];

export const FONCTIONNEMENT_FILTRE_OPTIONS: { value: FonctionnementFiltre | ''; label: string }[] = [
  { value: '', label: 'Sélectionner' },
  { value: 'En continu', label: 'En continu' },
  { value: 'Séquentiel', label: 'Séquentiel' },
];

export const LOCALISATION_OPTIONS: { value: PriseDeauRejetEau | ''; label: string }[] = [
  { value: '', label: 'Sélectionner' },
  { value: "Canal d'amené", label: "Canal d'amené" },
  { value: 'Large', label: 'Large' },
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
