import { GUILDE_ECOLOGIQUE_OPTIONS, REPARTITION_COLONNE_EAU_OPTIONS, GUILDE_TROPHIQUE_OPTIONS, ETAT_STOCK_OPTIONS, STATUT_PROTECTION_OPTIONS, CONSERVATION_OPTIONS, SENSIBILITE_LUMIERE_OPTIONS, SENSIBILITE_COURANT_OPTIONS, RESISTANCE_CHOCS_OPTIONS } from './poisson.constants';

// Réexporte les constantes partagées avec poissons
export {
  GUILDE_ECOLOGIQUE_OPTIONS,
  REPARTITION_COLONNE_EAU_OPTIONS,
  GUILDE_TROPHIQUE_OPTIONS,
  ETAT_STOCK_OPTIONS,
  STATUT_PROTECTION_OPTIONS,
  CONSERVATION_OPTIONS,
  SENSIBILITE_LUMIERE_OPTIONS,
  SENSIBILITE_COURANT_OPTIONS,
  RESISTANCE_CHOCS_OPTIONS,
};

export const GROUPE_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Céphalopode', label: 'Céphalopode' },
  { value: 'Crustacé', label: 'Crustacé' },
  { value: 'Bivalve', label: 'Bivalve' },
  { value: 'Poisson', label: 'Poisson' },
  { value: 'Annélide', label: 'Annélide' },
  { value: 'Cténaire', label: 'Cténaire' },
  { value: 'Gastéropode', label: 'Gastéropode' },
];

export const NON_POISSON_BADGE_COLORS: Record<string, string> = {
  'Céphalopode': 'badge-blue',
  'Crustacé':    'badge-teal',
  'Bivalve':     'badge-green',
  'Poisson':     'badge-cyan',
  'Annélide':    'badge-indigo',
  'Cténaire':    'badge-default',
  'Gastéropode': 'badge-blue',
};

export const FREQUENCE_OCCURRENCE_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Très fréquente', label: 'Très fréquente' },
  { value: 'Commune', label: 'Commune' },
  { value: 'Occasionnelle', label: 'Occasionnelle' },
  { value: 'Rare', label: 'Rare' },
  { value: 'NA', label: 'NA' },
];