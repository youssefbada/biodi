from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Poissons
from core.tests.mixins import AuthenticatedAdminMixin

class PoissonsApiTests(AuthenticatedAdminMixin, APITestCase):
  def setUp(self):
    super().setUp()
    self.poisson = Poissons.objects.create(
      famille="Anguillidae",
      genre="Anguilla",
      espece="anguilla",
      nom_commun="Anguille",
      guilde_ecologique="MJA",
      source_guilde_ecolo="Source 1",
      repartition_colonne_eau="Benthique",
      source_repartition_col_eau="Source 2",
      guilde_trophique="CAR",
      source_guilde_trophique="Source 3",
      interet_halieutique=True,
      source_interet_halieutique="Source 4",
      etat_stock="Reconstituable",
      source_etat_stock="Source 5",
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
      source_resistances="Source 11",
      comportement="Grégaire",
      source_comportement="Source 12",
      periode_reproduction="Printemps",
      forme_corps="Allongée",
      source_forme_corps="Source 13",
      type_peau="Lisse",
      source_type_peau="Source 14",
      locomotion="Amiiforme",
      source_locomotion="Source 15",
      endurance="Forte",
      source_endurance="Source 16",
      vitesse_croisiere_juvenile_ms="0.500",
      vitesse_soutenue_juvenile_ms="0.700",
      vitesse_sprint_juvenile_ms="1.100",
      vitesse_croisiere_adulte_ms="0.800",
      vitesse_soutenue_adulte_ms="1.000",
      vitesse_sprint_adulte_ms="1.400",
      source_vitesse_nage="Source 17",
    )

  def test_list_poissons_should_return_200(self):
    response = self.client.get("/api/poissons/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_detail_poisson_should_return_200(self):
    response = self.client.get(f"/api/poissons/{self.poisson.id_poisson}/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["nom_commun"], "Anguille")

  def test_detail_poisson_should_return_404_when_not_found(self):
    response = self.client.get("/api/poissons/99999/")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["code"], "POISSON_NOT_FOUND")

  def test_create_poisson_should_return_201(self):
    payload = {
      "famille": "Salmonidae",
      "genre": "Salmo",
      "espece": "trutta",
      "nom_commun": "Truite",
      "guilde_ecologique": "MJA",
      "source_guilde_ecolo": "S1",
      "repartition_colonne_eau": "Benthique",
      "source_repartition_col_eau": "S2",
      "guilde_trophique": "CAR",
      "source_guilde_trophique": "S3",
      "interet_halieutique": True,
      "source_interet_halieutique": "S4",
      "etat_stock": "Reconstituable",
      "source_etat_stock": "S5",
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
      "source_resistances": "S11",
      "comportement": "Grégaire",
      "source_comportement": "S12",
      "periode_reproduction": "Hiver",
      "forme_corps": "Fusiforme",
      "source_forme_corps": "S13",
      "type_peau": "Écailles",
      "source_type_peau": "S14",
      "locomotion": "Amiiforme",
      "source_locomotion": "S15",
      "endurance": "Fragile",
      "source_endurance": "S16",
      "vitesse_croisiere_juvenile_ms": "0.300",
      "vitesse_soutenue_juvenile_ms": "0.500",
      "vitesse_sprint_juvenile_ms": "0.900",
      "vitesse_croisiere_adulte_ms": "0.700",
      "vitesse_soutenue_adulte_ms": "0.900",
      "vitesse_sprint_adulte_ms": "1.200",
      "source_vitesse_nage": "S17"
    }

    response = self.client.post("/api/poissons/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Poissons.objects.count(), 2)

  def test_create_poisson_should_return_409_when_duplicate_triplet(self):
    payload = {
      "famille": "Anguillidae",
      "genre": "Anguilla",
      "espece": "anguilla",
      "nom_commun": "Anguille bis",
    }

    response = self.client.post("/api/poissons/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    self.assertEqual(response.data["code"], "POISSON_ALREADY_EXISTS")

  def test_update_poisson_should_return_200(self):
    payload = {
      "famille": "Anguillidae",
      "genre": "Anguilla",
      "espece": "anguilla",
      "nom_commun": "Anguille MAJ",
      "guilde_ecologique": "MJA",
      "source_guilde_ecolo": "Source 1",
      "repartition_colonne_eau": "Benthique",
      "source_repartition_col_eau": "Source 2",
      "guilde_trophique": "CAR",
      "source_guilde_trophique": "Source 3",
      "interet_halieutique": True,
      "source_interet_halieutique": "Source 4",
      "etat_stock": "Reconstituable",
      "source_etat_stock": "Source 5",
      "statut_protection": "Protégée",
      "source_protection": "Source 6",
      "conservation_fr": "LC",
      "conservation_eu": "LC",
      "conservation_md": "LC",
      "source_conservation": "Source 7",
      "sensibilite_lumiere": "Attraction",
      "source_sens_lumiere": "Source 8",
      "sensibilite_courants_eau": "Limnophile",
      "source_sens_courant": "Source 9",
      "sensibilite_sonore": "Modérée",
      "source_sens_sonore": "Source 10",
      "resistance_chocs_mecaniques": "Fragile",
      "resistance_chocs_chimiques": "Fragile",
      "resistance_chocs_thermiques": "Fragile",
      "source_resistances": "Source 11",
      "comportement": "Grégaire",
      "source_comportement": "Source 12",
      "periode_reproduction": "Printemps",
      "forme_corps": "Allongée",
      "source_forme_corps": "Source 13",
      "type_peau": "Lisse",
      "source_type_peau": "Source 14",
      "locomotion": "Amiiforme",
      "source_locomotion": "Source 15",
      "endurance": "Forte",
      "source_endurance": "Source 16",
      "vitesse_croisiere_juvenile_ms": "0.500",
      "vitesse_soutenue_juvenile_ms": "0.700",
      "vitesse_sprint_juvenile_ms": "1.100",
      "vitesse_croisiere_adulte_ms": "0.800",
      "vitesse_soutenue_adulte_ms": "1.000",
      "vitesse_sprint_adulte_ms": "1.400",
      "source_vitesse_nage": "Source 17",
    }

    response = self.client.put(f"/api/poissons/{self.poisson.id_poisson}/update/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.poisson.refresh_from_db()
    self.assertEqual(self.poisson.nom_commun, "Anguille MAJ")

  def test_partial_update_poisson_should_return_200(self):
    payload = {"nom_commun": "Anguille PATCH"}
    response = self.client.patch(f"/api/poissons/{self.poisson.id_poisson}/partial/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.poisson.refresh_from_db()
    self.assertEqual(self.poisson.nom_commun, "Anguille PATCH")

  def test_delete_poisson_should_return_204(self):
    response = self.client.delete(f"/api/poissons/{self.poisson.id_poisson}/delete/")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Poissons.objects.count(), 0)