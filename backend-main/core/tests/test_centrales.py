from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Centrales
from core.tests.mixins import AuthenticatedAdminMixin

class CentralesApiTests(AuthenticatedAdminMixin, APITestCase):
  def setUp(self):
    super().setUp()
    self.centrale = Centrales.objects.create(
      code_nom="GRA",
      site_name="Gravelines",
      milieu_type="Marin",
      source_froide="Mer du Nord",
      nbre_reacteurs=6,
      puissance_reacteurs_mwe=900,
      debit_aspire_par_tranche_m3s=42,
      debit_total_aspire_m3s=252,
      taux_disponibilite_moyen_tranches="Très bon",
      type_circuit="Ouvert",
      type_filtration="Tambour filtrant",
      dimension_filtre_h_l_m="10x5x3",
      maillage_mm=5,
      pression_nettoyage="Basse pression",
      traitement_chimique=True,
      type_traitement_chimique="Electrochloration",
      circuits_crf_sec_separes=True,
      pompes_separees=True,
      fonctionnement_filtre="En continu",
      temps_moyen_emersion_min=15,
      systeme_recuperation=True,
      presence_goulotte=True,
      goulotte_hauteur_eau=2,
      presence_pre_grille=True,
      espacement_pre_grille_mm=20,
      presence_canal_amenee=True,
      localisation_prise_eau="Large",
      localisation_rejet_eau="Large",
      profondeur_rejet_eau_m=3.500,
      distance_cote_rejet_eau_m=25.000,
      volume_eau_rejetee_m3s=12.50000,
      temperature_rejet_c=25,
      temperature_milieu_c=18,
      delta_t_c=7,
    )

  def test_list_centrales_should_return_200(self):
    response = self.client.get("/api/centrales/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_detail_centrale_should_return_200(self):
    response = self.client.get(f"/api/centrales/{self.centrale.id}/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["code_nom"], "GRA")

  def test_detail_centrale_should_return_404_when_not_found(self):
    response = self.client.get("/api/centrales/99999/")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["code"], "CENTRALE_NOT_FOUND")

  def test_create_centrale_should_return_201(self):
    payload = {
      "code_nom": "CIV",
      "site_name": "Civaux",
      "milieu_type": "Fleuve",
      "source_froide": "Vienne",
      "nbre_reacteurs": 2,
      "puissance_reacteurs_mwe": 1450,
      "debit_aspire_par_tranche_m3s": 50,
      "debit_total_aspire_m3s": 100,
      "taux_disponibilite_moyen_tranches": "Très bon",
      "type_circuit": "Fermé",
      "type_filtration": "Tambour filtrant",
      "dimension_filtre_h_l_m": "8x4x2",
      "maillage_mm": 4,
      "pression_nettoyage": "Basse pression",
      "traitement_chimique": True,
      "type_traitement_chimique": "Electrochloration",
      "circuits_crf_sec_separes": True,
      "pompes_separees": True,
      "fonctionnement_filtre": "En continu",
      "temps_moyen_emersion_min": 10,
      "systeme_recuperation": False,
      "presence_goulotte": False,
      "goulotte_hauteur_eau": None,
      "presence_pre_grille": True,
      "espacement_pre_grille_mm": 30,
      "presence_canal_amenee": True,
      "localisation_prise_eau": "Large",
      "localisation_rejet_eau": "Large",
      "profondeur_rejet_eau_m": "2.500",
      "distance_cote_rejet_eau_m": "15.000",
      "volume_eau_rejetee_m3s": "8.50000",
      "temperature_rejet_c": 22,
      "temperature_milieu_c": 17,
      "delta_t_c": 5,
    }

    response = self.client.post("/api/centrales/create/", payload, format="json")
    print(response.data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Centrales.objects.count(), 2)
    self.assertEqual(response.data["code_nom"], "CIV")

  def test_create_centrale_should_return_409_when_duplicate_code_nom(self):
    payload = {
      "code_nom": "GRA",
      "site_name": "Autre Gravelines",
      "type_circuit": "Ouvert",
    }

    response = self.client.post("/api/centrales/create/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    self.assertEqual(response.data["code"], "CENTRALE_ALREADY_EXISTS")

  def test_update_centrale_should_return_200(self):
    payload = {
       "code_nom": "CIV",
      "site_name": "Civaux MAJ",
      "milieu_type": "Fleuve",
      "source_froide": "Vienne",
      "nbre_reacteurs": 2,
      "puissance_reacteurs_mwe": 1450,
      "debit_aspire_par_tranche_m3s": 50,
      "debit_total_aspire_m3s": 100,
      "taux_disponibilite_moyen_tranches": "Très bon",
      "type_circuit": "Fermé",
      "type_filtration": "Tambour filtrant",
      "dimension_filtre_h_l_m": "8x4x2",
      "maillage_mm": 4,
      "pression_nettoyage": "Basse pression",
      "traitement_chimique": True,
      "type_traitement_chimique": "Electrochloration",
      "circuits_crf_sec_separes": True,
      "pompes_separees": True,
      "fonctionnement_filtre": "En continu",
      "temps_moyen_emersion_min": 10,
      "systeme_recuperation": False,
      "presence_goulotte": False,
      "goulotte_hauteur_eau": None,
      "presence_pre_grille": True,
      "espacement_pre_grille_mm": 30,
      "presence_canal_amenee": True,
      "localisation_prise_eau": "Large",
      "localisation_rejet_eau": "Large",
      "profondeur_rejet_eau_m": "2.500",
      "distance_cote_rejet_eau_m": "15.000",
      "volume_eau_rejetee_m3s": "8.50000",
      "temperature_rejet_c": 22,
      "temperature_milieu_c": 17,
      "delta_t_c": 5,
    }

    response = self.client.put(f"/api/centrales/{self.centrale.id}/update/", payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.centrale.refresh_from_db()
    self.assertEqual(self.centrale.site_name, "Civaux MAJ")

  def test_partial_update_centrale_should_return_200(self):
    payload = {
      "site_name": "Gravelines PATCH"
    }

    response = self.client.patch(f"/api/centrales/{self.centrale.id}/partial/", payload, format="json")
    print(response.data)
    print(payload)
    print(self.centrale.id)
    print(response.status_code)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.centrale.refresh_from_db()
    self.assertEqual(self.centrale.site_name, "Gravelines PATCH")

  def test_delete_centrale_should_return_204(self):
    response = self.client.delete(f"/api/centrales/{self.centrale.id}/delete/")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Centrales.objects.count(), 0)