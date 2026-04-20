from core.constants.error_codes import ErrorCodes

ERROR_MESSAGES = {

  ErrorCodes.CENTRALE_NOT_FOUND:
    "Centrale introuvable.",

  ErrorCodes.CENTRALE_ALREADY_EXISTS:
    "Une centrale avec ce code existe déjà.",

  ErrorCodes.POISSON_NOT_FOUND:
    "Poisson introuvable.",

  ErrorCodes.POISSON_ALREADY_EXISTS:
    "Un poisson avec cette famille, ce genre et cette espèce existe déjà.",

  ErrorCodes.NON_POISSON_NOT_FOUND:
    "Non poisson introuvable.",

  ErrorCodes.NON_POISSON_ALREADY_EXISTS:
    "Un non poisson avec ce groupe, cette famille, ce genre et cette espèce existe déjà.",

  ErrorCodes.ECHANTILLONNAGE_NOT_FOUND:
    "Echantillonnage introuvable.",

  ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS:
    "Un échantillonnage doit être lié à une centrale et à un seul type d'espèce : soit un poisson, soit un non-poisson.",


ErrorCodes.INVENTAIRE_NOT_FOUND:
    "Inventaire introuvable.",

  ErrorCodes.INVENTAIRE_INVALID_RELATIONS:
    "Un inventaire doit être lié à une centrale et à une seule espèce : soit un poisson, soit un non-poisson.",

  ErrorCodes.INVENTAIRE_ALREADY_EXISTS:
    "Un inventaire avec cette centrale et cette espèce existe déjà.",

  ErrorCodes.QUERY_BUILDER_INVALID_ROOT:
    "Table racine invalide pour le query builder.",

  ErrorCodes.QUERY_BUILDER_INVALID_RELATION:
    "Jointure invalide ou non autorisée.",

  ErrorCodes.QUERY_BUILDER_INVALID_FIELD:
    "Champ invalide ou non autorisé dans la requête.",

  ErrorCodes.QUERY_BUILDER_INVALID_OPERATOR:
    "Opérateur de filtre invalide.",

  ErrorCodes.QUERY_BUILDER_INVALID_FILTER:
    "Structure de filtre invalide.",

  ErrorCodes.QUERY_BUILDER_INVALID_LOGIC:
    "Opérateur logique invalide. Utiliser AND, OR ou NOT.",

  ErrorCodes.QUERY_BUILDER_INVALID_ORDER_BY:
    "Clause de tri invalide.",

  ErrorCodes.APP_USER_NOT_FOUND:
    "Utilisateur introuvable.",

  ErrorCodes.APP_USER_ALREADY_EXISTS:
    "Un utilisateur avec ce NNI ou cet email existe déjà.",

  ErrorCodes.APP_USER_INVALID_ROLE:
    "Rôle utilisateur invalide.",

  ErrorCodes.APP_USER_INACTIVE:
    "Cet utilisateur est inactif.",

  ErrorCodes.VALIDATION_ERROR:
    "Erreur de validation des données.",

  ErrorCodes.INTERNAL_ERROR:
    "Une erreur interne est survenue."
}
