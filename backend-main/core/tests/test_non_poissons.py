from rest_framework import status
from rest_framework.test import APITestCase

from core.models import NonPoissons
from core.tests.mixins import AuthenticatedAdminMixin

class NonPoissonsApiTests(AuthenticatedAdminMixin, APITestCase):
  def setUp(self):
    super().setUp()
    self.non_poisson = NonPoissons.objects.create(
      groupe="Crustacé",
      famille="Anguillidae",
      genre="Anguilla",
      espece="anguilla",
      nom_commun="Crevette",
      guilde_ecologique="MJA",
      source_guilde_ecolo="Source 1",
      repartition_colonne_eau="Benthique",
      source_repartition_col_eau="Source 2",
      guilde_trophique="CAR",
      source_guilde_trophique="Source 3",
      etat_stock="Reconstituable",
      source_stock="Source 5",
      statut_protection="Protégée",
      source_protection="Source 6",
      conservation_fr="LC",
      conservation_eu="LC",
      conservation_md="LC",
      source_conservation="Source 7",
      sensibilite_lumiere="Attraction",
      source_sens_lumiere="Source 8",
      sensibilite_courants_eau="Limnophile",
      source_sens_courant="Source 9",
      sensibilite_sonore="Modérée",
      source_sens_sonore="Source 10",
      resistance_chocs_mecaniques="Fragile",
      resistance_chocs_chimiques="Fragile",
      resistance_chocs_thermiques="Fragile",
      endurance="Forte",
      source_endurance="Source 16",
    )

  def test_list_non_poissons_should_return_200(self):
    response = self.client.get("/api/non-poissons/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_detail_non_poisson_should_return_200(self):
    response = self.client.get(f"/api/non-poissons/{self.non_poisson.id_non_poisson}/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["nom_commun"], "Crevette")

  def test_detail_non_poisson_should_return_404_when_not_found(self):
    response = self.client.get("/api/non-poissons/99999/")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["code"], "NON_POISSON_NOT_FOUND")

  def test_create_non_poisson_should_return_201(self):
    payload = {
      "groupe": "Crustacé",
      "famille": "Mytilidae",
      "genre": "Mytilus",
      "espece": "edulis",
      "nom_commun": "Moule",
      "guilde_ecologique": "MJA",
      "source_guilde_ecolo": "S1",
      "repartition_colonne_eau": "Benthique",
      "source_repartition_col_eau": "S2",
      "guilde_trophique": "CAR",
      "source_guilde_trophique": "S3",
      "enjeu_halieutique": True,
      "source_enjeu_halieutique": "S4",
      "etat_stock": "Reconstituable",
      "source_stock": "S5",
      "statut_protection": "Protégée",
      "source_protection": "S6",
      "conservation_fr": "LC",
      "conservation_eu": "LC",
      "conservation_md": "LC",
      "source_conservation": "S7",
      "sensibilite_lumiere": "Attraction",
      "source_sens_lumiere": "S8",
      "sensibilite_courants_eau": "Limnophile",
      "source_sens_courant": "S9",
      "sensibilite_sonore": "Faible",
      "source_sens_sonore": "S10",
      "resistance_chocs_mecaniques": "Fragile",
      "resistance_chocs_chimiques": "Fragile",
      "resistance_chocs_thermiques": "Fragile",
      "source_resistance_chocs": "S11",
      "endurance": "Faible",
      "source_endurance": "S12",
      "vitesse_nage_min_ms": "0.0000",
      "vitesse_nage_moy_ms": "0.0000",
      "vitesse_nage_max_ms": "0.0000",
      "source_vitesse_nage": "S13"
    }

    response = self.client.post("/api/non-poissons/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(NonPoissons.objects.count(), 2)

  def test_create_non_poisson_should_return_409_when_duplicate_triplet(self):
    payload = {
      "famille": "Anguillidae",
      "genre": "Anguilla",
      "espece": "anguilla",
    }

    response = self.client.post("/api/non-poissons/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    self.assertEqual(response.data["code"], "NON_POISSON_ALREADY_EXISTS")

  def test_update_non_poisson_should_return_200(self):
    payload = {
      "groupe": "Crustacé",
      "famille": "Palaemonidae",
      "genre": "Palaemon",
      "espece": "serratus",
      "nom_commun": "Crevette MAJ",
      "guilde_ecologique": "MJA",
      "source_guilde_ecolo": "S1",
      "repartition_colonne_eau": "Benthique",
      "source_repartition_col_eau": "S2",
      "guilde_trophique": "CAR",
      "source_guilde_trophique": "S3",
      "enjeu_halieutique": True,
      "source_enjeu_halieutique": "S4",
      "etat_stock": "Reconstituable",
      "source_stock": "S5",
      "statut_protection": "Protégée",
      "source_protection": "S6",
      "conservation_fr": "LC",
      "conservation_eu": "LC",
      "conservation_md": "LC",
      "source_conservation": "S7",
      "sensibilite_lumiere": "Attraction",
      "source_sens_lumiere": "S8",
      "sensibilite_courants_eau": "Limnophile",
      "source_sens_courant": "S9",
      "sensibilite_sonore": "Faible",
      "source_sens_sonore": "S10",
      "resistance_chocs_mecaniques": "Fragile",
      "resistance_chocs_chimiques": "Fragile",
      "resistance_chocs_thermiques": "Fragile",
      "source_resistance_chocs": "S11",
      "endurance": "Moyenne",
      "source_endurance": "S12",
      "vitesse_nage_min_ms": "0.1000",
      "vitesse_nage_moy_ms": "0.2000",
      "vitesse_nage_max_ms": "0.5000",
      "source_vitesse_nage": "S13",
    }

    response = self.client.put(f"/api/non-poissons/{self.non_poisson.id_non_poisson}/update/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.non_poisson.refresh_from_db()
    self.assertEqual(self.non_poisson.nom_commun, "Crevette MAJ")

  def test_partial_update_non_poisson_should_return_200(self):
    payload = {"nom_commun": "Crevette PATCH"}
    response = self.client.patch(f"/api/non-poissons/{self.non_poisson.id_non_poisson}/partial/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.non_poisson.refresh_from_db()
    self.assertEqual(self.non_poisson.nom_commun, "Crevette PATCH")

  def test_delete_non_poisson_should_return_204(self):
    response = self.client.delete(f"/api/non-poissons/{self.non_poisson.id_non_poisson}/delete/")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(NonPoissons.objects.count(), 0)