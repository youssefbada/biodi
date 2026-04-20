export const GUILDE_ECOLOGIQUE_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'AMP', label: 'AMP — Migrateur sans reproduction' },
  { value: 'ANA', label: 'ANA — Vit en mer, se reproduit en eau douce' },
  { value: 'CAT', label: 'CAT — Vit en eau douce, se reproduit en mer' },
  { value: 'FWR', label: 'FWR — Strictement dulçaquicole' },
  { value: 'ESR', label: 'ESR — Cycle en milieu estuarien' },
  { value: 'MAR', label: 'MAR — Strictement marine' },
  { value: 'MJA', label: 'MJA — Marine, juvéniles en estuaires' },
  { value: 'MAA', label: 'MAA — Marine, parties basses estuaires' },
];

export const REPARTITION_COLONNE_EAU_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Benthique', label: 'Benthique' },
  { value: 'Démersale', label: 'Démersale' },
  { value: 'Pélagique', label: 'Pélagique' },
];

export const GUILDE_TROPHIQUE_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'CAR', label: 'CAR — Invertébrés et poissons' },
  { value: 'HERB', label: 'HERB — Algues et végétaux' },
  { value: 'INV', label: 'INV — Invertébrés' },
  { value: 'OMN', label: 'OMN — Omnivore' },
  { value: 'PISC', label: 'PISC — Poissons' },
  { value: 'PLC', label: 'PLC — Zooplancton' },
  { value: 'NA', label: 'NA' },
  { value: 'Autre', label: 'Autre' },
];

export const ETAT_STOCK_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Bon état', label: 'Bon état' },
  { value: 'Reconstituable', label: 'Reconstituable' },
  { value: 'Surpêché', label: 'Surpêché' },
  { value: 'Surpêché et dégradé', label: 'Surpêché et dégradé' },
  { value: 'Effondré', label: 'Effondré' },
  { value: 'Non classifié', label: 'Non classifié' },
  { value: 'Non évalué', label: 'Non évalué' },
];

export const STATUT_PROTECTION_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Protégée', label: 'Protégée' },
  { value: 'Non protégée', label: 'Non protégée' },
];

export const CONSERVATION_OPTIONS = [
  { value: '', label: '—' },
  { value: 'EX', label: 'EX — Éteint' },
  { value: 'EW', label: 'EW — Éteint à l\'état sauvage' },
  { value: 'CR', label: 'CR — En danger critique' },
  { value: 'EN', label: 'EN — En danger' },
  { value: 'VU', label: 'VU — Vulnérable' },
  { value: 'NT', label: 'NT — Quasi menacé' },
  { value: 'LC', label: 'LC — Préoccupation mineure' },
  { value: 'DD', label: 'DD — Données insuffisantes' },
  { value: 'NE', label: 'NE — Non évalué' },
  { value: 'NA', label: 'NA — Non applicable' },
];

export const SENSIBILITE_LUMIERE_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Attraction', label: 'Attraction' },
  { value: 'Répulsion', label: 'Répulsion' },
];

export const SENSIBILITE_COURANT_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Limnophile', label: 'Limnophile' },
  { value: 'Rhéophile', label: 'Rhéophile' },
];

export const RESISTANCE_CHOCS_OPTIONS = [
  { value: '', label: '—' },
  { value: 'Fragile', label: 'Fragile' },
  { value: 'Robuste', label: 'Robuste' },
];

export const COMPORTEMENT_OPTIONS = [
  { value: '', label: 'Tous' },
  { value: 'Grégaire', label: 'Grégaire' },
  { value: 'Solitaire', label: 'Solitaire' },
];

export const FORME_CORPS_OPTIONS = [
  { value: '', label: '—' },
  { value: 'Allongée', label: 'Allongée' },
  { value: 'Anguilliforme', label: 'Anguilliforme' },
  { value: 'Compressiforme', label: 'Compressiforme' },
  { value: 'Dépressiforme', label: 'Dépressiforme' },
  { value: 'Filiforme', label: 'Filiforme' },
  { value: 'Fusiforme', label: 'Fusiforme' },
  { value: 'Globiforme', label: 'Globiforme' },
  { value: 'Autre', label: 'Autre' },
];

export const LOCOMOTION_OPTIONS = [
  { value: '', label: '—' },
  { value: 'Amiiforme', label: 'Amiiforme' },
  { value: 'Anguilliforme', label: 'Anguilliforme' },
  { value: 'Balistiforme', label: 'Balistiforme' },
  { value: 'Carangiforme', label: 'Carangiforme' },
  { value: 'Diodontiforme', label: 'Diodontiforme' },
  { value: 'Gymnotiforme', label: 'Gymnotiforme' },
  { value: 'Labriforme', label: 'Labriforme' },
  { value: 'Ostraciiforme', label: 'Ostraciiforme' },
  { value: 'Rajiforme', label: 'Rajiforme' },
  { value: 'Sous-carangiforme', label: 'Sous-carangiforme' },
  { value: 'Tétraodontiforme', label: 'Tétraodontiforme' },
  { value: 'Thunniforme', label: 'Thunniforme' },
];

export const POISSON_BADGE_COLORS: Record<string, string> = {
  AMP: 'badge-blue',
  ANA: 'badge-green',
  CAT: 'badge-teal',
  FWR: 'badge-cyan',
  ESR: 'badge-indigo',
  MAR: 'badge-blue',
  MJA: 'badge-green',
  MAA: 'badge-teal',
};