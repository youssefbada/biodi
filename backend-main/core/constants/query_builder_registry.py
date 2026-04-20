from dataclasses import dataclass
from typing import Dict, Type

from core.models import (
  Centrales,
  Poissons,
  NonPoissons,
  Echantillonnage,
  InventaireMilieu,
)


@dataclass(frozen=True)
class RelationConfig:
  target_key: str
  orm_name: str


@dataclass(frozen=True)
class ModelConfig:
  key: str
  label: str
  model: Type
  relations: Dict[str, RelationConfig]


QUERY_BUILDER_MODELS: Dict[str, ModelConfig] = {
  "centrales": ModelConfig(
    key="centrales",
    label="Centrales",
    model=Centrales,
    relations={
      "echantillonnages": RelationConfig(
        target_key="echantillonnages",
        orm_name="echantillonnages",
      ),
      "inventaires": RelationConfig(
        target_key="inventaires_milieu",
        orm_name="inventaires",
      ),
    },
  ),
  "poissons": ModelConfig(
    key="poissons",
    label="Poissons",
    model=Poissons,
    relations={
      "echantillonnages": RelationConfig(
        target_key="echantillonnages",
        orm_name="echantillonnages",
      ),
      "inventaires": RelationConfig(
        target_key="inventaires_milieu",
        orm_name="inventaires_milieu",
      ),
    },
  ),
  "non_poissons": ModelConfig(
    key="non_poissons",
    label="Non-poissons",
    model=NonPoissons,
    relations={
      "echantillonnages": RelationConfig(
        target_key="echantillonnages",
        orm_name="echantillonnages",
      ),
      "inventaires": RelationConfig(
        target_key="inventaires_milieu",
        orm_name="inventaires_milieu",
      ),
    },
  ),
  "echantillonnages": ModelConfig(
    key="echantillonnages",
    label="Echantillonnages",
    model=Echantillonnage,
    relations={
      "centrale": RelationConfig(
        target_key="centrales",
        orm_name="centrale",
      ),
      "poisson": RelationConfig(
        target_key="poissons",
        orm_name="poisson",
      ),
      "non_poisson": RelationConfig(
        target_key="non_poissons",
        orm_name="non_poisson",
      ),
    },
  ),
  "inventaires_milieu": ModelConfig(
    key="inventaires_milieu",
    label="Inventaires milieu",
    model=InventaireMilieu,
    relations={
      "centrale": RelationConfig(
        target_key="centrales",
        orm_name="centrale",
      ),
      "espece_poisson": RelationConfig(
        target_key="poissons",
        orm_name="espece_poisson",
      ),
      "espece_non_poisson": RelationConfig(
        target_key="non_poissons",
        orm_name="espece_non_poisson",
      ),
    },
  ),
}


def get_model_config(model_key: str) -> ModelConfig:
  if model_key not in QUERY_BUILDER_MODELS:
    raise ValueError(f"Unknown model key: {model_key}")
  return QUERY_BUILDER_MODELS[model_key]