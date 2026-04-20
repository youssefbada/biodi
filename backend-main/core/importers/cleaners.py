from decimal import Decimal, InvalidOperation
import re

TRUE_SET = {"1", "true", "vrai", "oui", "y", "yes"}
FALSE_SET = {"0", "false", "faux", "non", "n", "no"}


def strip_or_empty(value):
    if value is None:
        return ""
    return str(value).strip()


def strip_or_none(value):
    v = strip_or_empty(value)
    return v if v != "" else None


def to_bool(value):
    v = strip_or_empty(value).lower()
    if v == "":
        return None
    if v in TRUE_SET:
        return True
    if v in FALSE_SET:
        return False
    # parfois Access met -1 pour True
    if v == "-1":
        return True
    raise ValueError(f"Valeur bool invalide: {value}")


def to_decimal(value):
    v = strip_or_empty(value)
    if v == "":
        return None
    # remplace virgule
    v = v.replace(",", ".")
    # supprime espaces
    v = re.sub(r"\s+", "", v)
    try:
        return Decimal(v)
    except InvalidOperation:
        raise ValueError(f"Valeur decimal invalide: {value}")


def to_int(value):
    v = strip_or_empty(value)
    if v == "":
        return None
    v = v.replace(",", ".")
    return int(float(v))


def normalize_enum(value, enum_cls):
    """
    Retourne la valeur EXACTE attendue par TextChoices, en tolérant accents/casse.
    Ex: 'riviere' -> 'Rivière' (si enum contient cette valeur)
    """
    v = strip_or_empty(value)
    if v == "":
        return ""
    v_norm = v.casefold()

    # essaye match sur value et label
    for choice_value, choice_label in enum_cls.choices:
        if choice_value.casefold() == v_norm or choice_label.casefold() == v_norm:
            return choice_value

    raise ValueError(f"Valeur enum invalide '{value}' pour {enum_cls.__name__}")


def strip_upper_or_none(value):
    v = strip_or_none(value)
    return v.upper() if v else None
