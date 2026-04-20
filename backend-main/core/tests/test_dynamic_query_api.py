from django.test import TestCase
from rest_framework.test import APIClient

from core.models import (
  Centrales,
  Poissons,
  NonPoissons,
  Echantillonnage,
  InventaireMilieu,
)
from core.tests.mixins import AuthenticatedAdminMixin, AuthenticatedUserMixin

class DynamicQueryApiTests(AuthenticatedAdminMixin, TestCase):
  def setUp(self):
    super().setUp()
    # self.client = APIClient()

    # ----------------------------
    # Centrales
    # ----------------------------
    self.centrale_gra = Centrales.objects.create(
      code_nom="GRA",
      site_name="Gravelines",
      source_froide="Mer du Nord",
    )
    self.centrale_civ = Centrales.objects.create(
      code_nom="CIV",
      site_name="Civaux",
      source_froide="Vienne",
    )

    # ----------------------------
    # Poissons
    # ----------------------------
    self.poisson_anguille = Poissons.objects.create(
      famille="Anguillidae",
      genre="Anguilla",
      espece="anguilla",
      nom_commun="Anguille",
    )
    self.poisson_truite = Poissons.objects.create(
      famille="Salmonidae",
      genre="Salmo",
      espece="trutta",
      nom_commun="Truite",
    )

    # ----------------------------
    # Non poissons
    # ----------------------------
    self.non_poisson_crevette = NonPoissons.objects.create(
      groupe="Crustacés",
      famille="Palaemonidae",
      genre="Palaemon",
      espece="serratus",
      nom_commun="Crevette",
    )

    # ----------------------------
    # Echantillonnages
    # ----------------------------
    self.ech_1 = Echantillonnage.objects.create(
      centrale=self.centrale_gra,
      poisson=self.poisson_anguille,
      groupe="Poissons",
      date_echantillonnage="1981-03-17",
      nombre_echantillonnage=10,
      duree_echantillonnage_min=45,
      debris_vegetaux=True,
      juveniles_nombre_individus=5,
      adultes_nombre_individus=2,
    )

    self.ech_2 = Echantillonnage.objects.create(
      centrale=self.centrale_civ,
      poisson=self.poisson_truite,
      groupe="Poissons",
      date_echantillonnage="1982-05-10",
      nombre_echantillonnage=20,
      duree_echantillonnage_min=30,
      debris_vegetaux=False,
      juveniles_nombre_individus=1,
      adultes_nombre_individus=8,
    )

    self.ech_3 = Echantillonnage.objects.create(
      centrale=self.centrale_gra,
      non_poisson=self.non_poisson_crevette,
      groupe="Crustacés",
      date_echantillonnage="1983-01-01",
      nombre_echantillonnage=15,
      duree_echantillonnage_min=25,
      debris_vegetaux=None,
    )

    # ----------------------------
    # Inventaires milieu
    # ----------------------------
    self.inv_1 = InventaireMilieu.objects.create(
      centrale=self.centrale_gra,
      espece_poisson=self.poisson_anguille,
      nom_commun="Anguille",
      groupe_poisson="Poissons",
    )
    self.inv_2 = InventaireMilieu.objects.create(
      centrale=self.centrale_civ,
      espece_non_poisson=self.non_poisson_crevette,
      nom_commun="Crevette",
      groupe_non_poisson="Crustacés",
    )

    self.metadata_url = "/api/query-builder/metadata/"
    self.execute_url = "/api/query-builder/execute/"

  # ==========================================================
  # METADATA
  # ==========================================================
  def test_metadata_should_return_200(self):
    response = self.client.get(self.metadata_url)

    self.assertEqual(response.status_code, 200)
    self.assertIn("roots", response.data)
    self.assertTrue(len(response.data["roots"]) >= 5)

  def test_metadata_should_contain_expected_roots(self):
    response = self.client.get(self.metadata_url)

    self.assertEqual(response.status_code, 200)
    root_keys = {item["key"] for item in response.data["roots"]}

    self.assertIn("centrales", root_keys)
    self.assertIn("poissons", root_keys)
    self.assertIn("non_poissons", root_keys)
    self.assertIn("echantillonnages", root_keys)
    self.assertIn("inventaires_milieu", root_keys)

  # ==========================================================
  # EXECUTE - BASE
  # ==========================================================
  def test_execute_should_return_200_with_simple_select(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "id_echantillonnage",
        "date_echantillonnage",
        "centrale.code_nom",
        "centrale.site_name",
      ],
      "limit": 10,
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["root"], "echantillonnages")
    self.assertIn("columns", response.data)
    self.assertIn("rows", response.data)
    self.assertGreaterEqual(response.data["count"], 1)

  def test_execute_should_return_selected_columns_only(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
        "site_name",
      ],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    first_row = response.data["rows"][0]
    self.assertIn("code_nom", first_row)
    self.assertIn("site_name", first_row)

  # ==========================================================
  # FILTERS - EQ / NEQ
  # ==========================================================
  def test_execute_filter_eq(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "centrale.code_nom",
        "poisson.nom_commun",
      ],
      "filters": {
        "field": "centrale.code_nom",
        "operator": "eq",
        "value": "GRA",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 2)
    for row in response.data["rows"]:
      self.assertEqual(row["centrale.code_nom"], "GRA")

  def test_execute_filter_neq(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
      ],
      "filters": {
        "field": "code_nom",
        "operator": "neq",
        "value": "GRA",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    returned_values = [row["code_nom"] for row in response.data["rows"]]
    self.assertNotIn("GRA", returned_values)

  # ==========================================================
  # FILTERS - GT / GTE / LT / LTE
  # ==========================================================
  def test_execute_filter_gt(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "nombre_echantillonnage",
      ],
      "filters": {
        "field": "nombre_echantillonnage",
        "operator": "gt",
        "value": 12,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    for row in response.data["rows"]:
      self.assertTrue(row["nombre_echantillonnage"] > 12)

  def test_execute_filter_gte(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "nombre_echantillonnage",
      ],
      "filters": {
        "field": "nombre_echantillonnage",
        "operator": "gte",
        "value": 15,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    for row in response.data["rows"]:
      self.assertTrue(row["nombre_echantillonnage"] >= 15)

  def test_execute_filter_lt(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "nombre_echantillonnage",
      ],
      "filters": {
        "field": "nombre_echantillonnage",
        "operator": "lt",
        "value": 20,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    for row in response.data["rows"]:
      self.assertTrue(row["nombre_echantillonnage"] < 20)

  def test_execute_filter_lte(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "nombre_echantillonnage",
      ],
      "filters": {
        "field": "nombre_echantillonnage",
        "operator": "lte",
        "value": 15,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    for row in response.data["rows"]:
      self.assertTrue(row["nombre_echantillonnage"] <= 15)

  # ==========================================================
  # FILTERS - contains / icontains
  # ==========================================================
  def test_execute_filter_contains(self):
    payload = {
      "root": "centrales",
      "select": [
        "site_name",
      ],
      "filters": {
        "field": "site_name",
        "operator": "contains",
        "value": "avel",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 1)
    self.assertEqual(response.data["rows"][0]["site_name"], "Gravelines")

  def test_execute_filter_icontains(self):
    payload = {
      "root": "poissons",
      "select": [
        "nom_commun",
      ],
      "filters": {
        "field": "nom_commun",
        "operator": "icontains",
        "value": "ang",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    values = [row["nom_commun"] for row in response.data["rows"]]
    self.assertIn("Anguille", values)

  # ==========================================================
  # FILTERS - startswith / endswith
  # ==========================================================
  def test_execute_filter_startswith(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
      ],
      "filters": {
        "field": "code_nom",
        "operator": "startswith",
        "value": "GR",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["rows"][0]["code_nom"], "GRA")

  def test_execute_filter_endswith(self):
    payload = {
      "root": "centrales",
      "select": [
        "site_name",
      ],
      "filters": {
        "field": "site_name",
        "operator": "endswith",
        "value": "aux",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["rows"][0]["site_name"], "Civaux")

  # ==========================================================
  # FILTERS - in
  # ==========================================================
  def test_execute_filter_in(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
      ],
      "filters": {
        "field": "code_nom",
        "operator": "in",
        "value": ["GRA", "CIV"],
      },
      "order_by": [{"field": "code_nom", "direction": "asc"}],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    values = [row["code_nom"] for row in response.data["rows"]]
    self.assertEqual(values, ["CIV", "GRA"])

  # ==========================================================
  # FILTERS - isnull
  # ==========================================================
  def test_execute_filter_isnull_true(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "id_echantillonnage",
        "debris_vegetaux",
      ],
      "filters": {
        "field": "debris_vegetaux",
        "operator": "isnull",
        "value": True,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 1)

  def test_execute_filter_isnull_false(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "id_echantillonnage",
        "debris_vegetaux",
      ],
      "filters": {
        "field": "debris_vegetaux",
        "operator": "isnull",
        "value": False,
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertGreaterEqual(response.data["count"], 2)

  # ==========================================================
  # LOGIC - AND / OR / NOT
  # ==========================================================
  def test_execute_filter_logic_and(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "centrale.code_nom",
        "nombre_echantillonnage",
      ],
      "filters": {
        "logic": "AND",
        "conditions": [
          {
            "field": "centrale.code_nom",
            "operator": "eq",
            "value": "GRA",
          },
          {
            "field": "nombre_echantillonnage",
            "operator": "gte",
            "value": 10,
          },
        ],
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 2)

  def test_execute_filter_logic_or(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "centrale.code_nom",
        "poisson.nom_commun",
      ],
      "filters": {
        "logic": "OR",
        "conditions": [
          {
            "field": "centrale.code_nom",
            "operator": "eq",
            "value": "CIV",
          },
          {
            "field": "poisson.nom_commun",
            "operator": "eq",
            "value": "Anguille",
          },
        ],
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertGreaterEqual(response.data["count"], 2)

  def test_execute_filter_logic_not(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
      ],
      "filters": {
        "logic": "NOT",
        "conditions": [
          {
            "field": "code_nom",
            "operator": "eq",
            "value": "GRA",
          }
        ],
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    values = [row["code_nom"] for row in response.data["rows"]]
    self.assertNotIn("GRA", values)

  # ==========================================================
  # JOINS
  # ==========================================================
  def test_execute_join_from_echantillonnages_to_centrale(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "centrale.code_nom",
        "centrale.site_name",
      ],
      "limit": 10,
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertIn("centrale.code_nom", response.data["rows"][0])
    self.assertIn("centrale.site_name", response.data["rows"][0])

  def test_execute_join_from_inventaires_to_poisson(self):
    payload = {
      "root": "inventaires_milieu",
      "select": [
        "centrale.site_name",
        "espece_poisson.nom_commun",
      ],
      "filters": {
        "field": "espece_poisson.nom_commun",
        "operator": "eq",
        "value": "Anguille",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 1)

  def test_execute_join_from_inventaires_to_non_poisson(self):
    payload = {
      "root": "inventaires_milieu",
      "select": [
        "centrale.site_name",
        "espece_non_poisson.nom_commun",
      ],
      "filters": {
        "field": "espece_non_poisson.nom_commun",
        "operator": "eq",
        "value": "Crevette",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 1)

  # ==========================================================
  # ORDER BY / LIMIT / DISTINCT
  # ==========================================================
  def test_execute_order_by_desc(self):
    payload = {
      "root": "centrales",
      "select": [
        "code_nom",
      ],
      "order_by": [
        {
          "field": "code_nom",
          "direction": "desc",
        }
      ],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    values = [row["code_nom"] for row in response.data["rows"]]
    self.assertEqual(values, sorted(values, reverse=True))

  def test_execute_limit(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "id_echantillonnage",
      ],
      "limit": 1,
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["count"], 1)
    self.assertEqual(len(response.data["rows"]), 1)

  def test_execute_distinct(self):
    payload = {
      "root": "echantillonnages",
      "select": [
        "centrale.code_nom",
      ],
      "distinct": True,
      "order_by": [
        {
          "field": "centrale.code_nom",
          "direction": "asc",
        }
      ],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 200)
    values = [row["centrale.code_nom"] for row in response.data["rows"]]
    self.assertEqual(values, ["CIV", "GRA"])

  # ==========================================================
  # ERRORS
  # ==========================================================
  def test_execute_should_fail_when_root_is_invalid(self):
    payload = {
      "root": "table_inconnue",
      "select": ["id"],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_ROOT")

  def test_execute_should_fail_when_field_is_invalid(self):
    payload = {
      "root": "centrales",
      "select": ["champ_invalide"],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_FIELD")

  def test_execute_should_fail_when_relation_is_invalid(self):
    payload = {
      "root": "centrales",
      "select": ["poisson.nom_commun"],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_RELATION")

  def test_execute_should_fail_when_operator_is_invalid(self):
    payload = {
      "root": "centrales",
      "select": ["code_nom"],
      "filters": {
        "field": "code_nom",
        "operator": "LIKE_SQL",
        "value": "GRA",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_OPERATOR")

  def test_execute_should_fail_when_logic_is_invalid(self):
    payload = {
      "root": "centrales",
      "select": ["code_nom"],
      "filters": {
        "logic": "XOR",
        "conditions": [
          {
            "field": "code_nom",
            "operator": "eq",
            "value": "GRA",
          }
        ],
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_LOGIC")

  def test_execute_should_fail_when_filter_is_malformed(self):
    payload = {
      "root": "centrales",
      "select": ["code_nom"],
      "filters": {
        "operator": "eq",
        "value": "GRA",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_FILTER")

  def test_execute_should_fail_when_order_by_is_invalid(self):
    payload = {
      "root": "centrales",
      "select": ["code_nom"],
      "order_by": [
        {
          "field": "code_nom",
          "direction": "sideways",
        }
      ],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_ORDER_BY")

  def test_execute_should_fail_when_select_is_empty(self):
    payload = {
      "root": "centrales",
      "select": [],
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 400)

  def test_execute_should_fail_when_in_value_is_not_list(self):
    payload = {
      "root": "centrales",
      "select": ["code_nom"],
      "filters": {
        "field": "code_nom",
        "operator": "in",
        "value": "GRA",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_FILTER")

  def test_execute_should_fail_when_isnull_value_is_not_bool(self):
    payload = {
      "root": "echantillonnages",
      "select": ["id_echantillonnage"],
      "filters": {
        "field": "debris_vegetaux",
        "operator": "isnull",
        "value": "true",
      },
    }

    response = self.client.post(self.execute_url, data=payload, format="json")

    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.data["code"], "QUERY_BUILDER_INVALID_FILTER")