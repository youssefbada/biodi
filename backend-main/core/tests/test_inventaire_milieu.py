from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Centrales, Poissons, NonPoissons, InventaireMilieu
from core.tests.mixins import AuthenticatedAdminMixin

class InventairesMilieuApiTests(AuthenticatedAdminMixin, APITestCase):
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
      nom_commun="Anguille",
    )

    self.inventaire = InventaireMilieu.objects.create(
      centrale=self.centrale,
      espece_poisson=self.poisson,
      nom_commun="Anguille",
      groupe_poisson="Crustacé",
      groupe_non_poisson="",
    )

  def test_list_inventaires_should_return_200(self):
    response = self.client.get("/api/inventaires-milieu/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_detail_inventaire_should_return_200(self):
    response = self.client.get(f"/api/inventaires-milieu/{self.inventaire.id_inventaire}/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["centrale_id"], self.centrale.id)

  def test_detail_inventaire_should_return_404_when_not_found(self):
    response = self.client.get("/api/inventaires-milieu/99999/")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["code"], "INVENTAIRE_NOT_FOUND")

#   def test_create_inventaire_with_poisson_should_return_201(self):
#     # payload = {
#     #   "centrale_id": self.centrale.id,
#     #   "espece_non_poisson_id": 2,
#     #   "nom_commun": "Anguille",
#     #   "groupe_poisson": "Crustacé",
#     #   "groupe_non_poisson": "",
#     # }

#     # response = self.client.post("/api/inventaires-milieu/create/", payload, format="json")
#     # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     self.assertEqual(InventaireMilieu.objects.count(), 2)

  def test_create_inventaire_with_non_poisson_should_return_201(self):
    payload = {
      "centrale_id": self.centrale.id,
      "espece_non_poisson_id": self.non_poisson.id_non_poisson,
      "nom_commun": "Crevette",
      "groupe_poisson": "",
      "groupe_non_poisson": "Crustacé",
    }

    response = self.client.post("/api/inventaires-milieu/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_inventaire_should_return_409_when_both_species_are_sent(self):
    payload = {
      "centrale_id": self.centrale.id,
      "espece_poisson_id": self.poisson.id_poisson,
      "espece_non_poisson_id": self.non_poisson.id_non_poisson,
      "nom_commun": "Erreur",
      "groupe_poisson": "Crustacé",
      "groupe_non_poisson": "Crustacé",
    }

    response = self.client.post("/api/inventaires-milieu/create/", payload, format="json")
    self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

  def test_update_inventaire_should_return_200(self):
    payload = {
      "centrale_id": self.centrale.id,
      "espece_poisson_id": self.poisson.id_poisson,
      "nom_commun": "Anguille MAJ",
      "groupe_poisson": "Crustacé",
      "groupe_non_poisson": "",
    }

    response = self.client.put(
      f"/api/inventaires-milieu/{self.inventaire.id_inventaire}/update/",
      payload,
      format="json",
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.inventaire.refresh_from_db()
    self.assertEqual(self.inventaire.nom_commun, "Anguille MAJ")

  def test_partial_update_inventaire_should_return_200(self):
    payload = {
      "nom_commun": "Anguille PATCH",
      "espece_poisson_id": self.poisson.id_poisson,
    }

    response = self.client.patch(
      f"/api/inventaires-milieu/{self.inventaire.id_inventaire}/partial/",
      payload,
      format="json",
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.inventaire.refresh_from_db()
    self.assertEqual(self.inventaire.nom_commun, "Anguille PATCH")

  def test_delete_inventaire_should_return_204(self):
    response = self.client.delete(
      f"/api/inventaires-milieu/{self.inventaire.id_inventaire}/delete/"
    )
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(InventaireMilieu.objects.count(), 0)