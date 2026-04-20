from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Centrales, Poissons, NonPoissons, Echantillonnage
from core.tests.mixins import AuthenticatedAdminMixin

class EchantillonnagesApiTests(AuthenticatedAdminMixin, APITestCase):
  def setUp(self):
    super().setUp()
    self.centrale = Centrales.objects.create(
      code_nom="GRA",
      site_name="Gravelines",
      type_circuit="Ouvert",
      maillage_mm=5,
    )

    self.poisson = Poissons.objects.create(
      famille="Anguillidae",
      genre="Anguilla",
      espece="anguilla",
      nom_commun="Anguille",
    )

    self.non_poisson = NonPoissons.objects.create(
      groupe="Crustacé",
      famille="Palaemonidae",
      genre="Palaemon",
      espece="serratus",
      nom_commun="Crevette",
    )

    self.echantillonnage = Echantillonnage.objects.create(
      centrale=self.centrale,
      date_echantillonnage="2024-01-10",
      nombre_echantillonnage=10,
      duree_echantillonnage_min=30,
      debris_vegetaux=True,
      groupe="Crustacé",
      poisson=self.poisson,
      frequence_occurrence="Rare",
      juveniles_nombre_individus=3,
      adultes_nombre_individus=2,
      totaux_nombre_individus=5,
      hiver_nombre_echantillonnage="1",
      printemps_nombre_echantillonnage="2",
      ete_nombre_echantillonnage="3",
      automne_nombre_echantillonnage="4",
      sources="Source test",
    )

  def test_list_echantillonnages_should_return_200(self):
    response = self.client.get("/api/echantillonnages/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_detail_echantillonnage_should_return_200(self):
    response = self.client.get(f"/api/echantillonnages/{self.echantillonnage.id_echantillonnage}/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["centrale_id"], self.centrale.id)

  def test_detail_echantillonnage_should_return_404_when_not_found(self):
    response = self.client.get("/api/echantillonnages/99999/")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["code"], "ECHANTILLONNAGE_NOT_FOUND")

  def test_create_echantillonnage_with_poisson_should_return_201(self):
    payload = {
      "centrale_id": self.centrale.id,
      "date_echantillonnage": "2024-02-01",
      "nombre_echantillonnage": 20,
      "duree_echantillonnage_min": 45,
      "debris_vegetaux": False,
      "groupe": "Crustacé",
      "poisson_id": self.poisson.id_poisson,
      "frequence_occurrence": "Rare",
      "hiver_nombre_echantillonnage": "1",
      "printemps_nombre_echantillonnage": "1",
      "ete_nombre_echantillonnage": "1",
      "automne_nombre_echantillonnage": "1",
      "sources": "Create test",
    }

    response = self.client.post("/api/echantillonnages/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Echantillonnage.objects.count(), 2)

  def test_create_echantillonnage_with_non_poisson_should_return_201(self):
    payload = {
      "centrale_id": self.centrale.id,
      "date_echantillonnage": "2024-02-01",
      "nombre_echantillonnage": 20,
      "duree_echantillonnage_min": 45,
      "debris_vegetaux": False,
      "groupe": "Crustacé",
      "non_poisson_id": self.non_poisson.id_non_poisson,
      "frequence_occurrence": "Rare",
      "hiver_nombre_echantillonnage": "1",
      "printemps_nombre_echantillonnage": "1",
      "ete_nombre_echantillonnage": "1",
      "automne_nombre_echantillonnage": "1",
      "sources": "Create test",
    }

    response = self.client.post("/api/echantillonnages/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_echantillonnage_should_return_409_when_both_species_are_sent(self):
    payload = {
      "centrale_id": self.centrale.id,
      "poisson_id": self.poisson.id_poisson,
      "non_poisson_id": self.non_poisson.id_non_poisson,
    }

    response = self.client.post("/api/echantillonnages/create/", payload, format="json")
    self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

  def test_update_echantillonnage_should_return_200(self):
    payload = {
      "centrale_id": self.centrale.id,
      "date_echantillonnage": "2024-03-01",
      "nombre_echantillonnage": 99,
      "duree_echantillonnage_min": 50,
      "debris_vegetaux": False,
      "groupe": "Crustacé",
      "poisson_id": self.poisson.id_poisson,
      "frequence_occurrence": "Rare",
      "hiver_nombre_echantillonnage": "2",
      "printemps_nombre_echantillonnage": "2",
      "ete_nombre_echantillonnage": "2",
      "automne_nombre_echantillonnage": "2",
      "sources": "Update test",
    }

    response = self.client.put(
      f"/api/echantillonnages/{self.echantillonnage.id_echantillonnage}/update/",
      payload,
      format="json",
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.echantillonnage.refresh_from_db()
    self.assertEqual(self.echantillonnage.nombre_echantillonnage, 99)

  def test_partial_update_echantillonnage_should_return_200(self):
    payload = {
      "sources": "PATCH test",
      "poisson_id": self.poisson.id_poisson,
      "nombre_echantillonnage": 77,
    }

    response = self.client.patch(
      f"/api/echantillonnages/{self.echantillonnage.id_echantillonnage}/partial/",
      payload,
      format="json",
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.echantillonnage.refresh_from_db()
    self.assertEqual(self.echantillonnage.nombre_echantillonnage, 77)

  def test_delete_echantillonnage_should_return_204(self):
    response = self.client.delete(
      f"/api/echantillonnages/{self.echantillonnage.id_echantillonnage}/delete/"
    )
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Echantillonnage.objects.count(), 0)