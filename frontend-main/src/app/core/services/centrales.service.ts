import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Centrale, CentraleFilters } from '../../models/centrale.model';
import { ExportService } from './export.service';
import { ImportService, ImportResult } from './import.service';

@Injectable({
 providedIn: 'root',
})
export class CentralesService {
 private http = inject(HttpClient);
 private exportService = inject(ExportService);
 private importService = inject(ImportService);

 private readonly baseUrl = `${environment.apiBaseUrl}/centrales`;

 // ─── GET ALL ───
 getAll(filters: CentraleFilters = {}): Observable<Centrale[]> {
  let params = new HttpParams();
  if (filters.search) params = params.set('search', filters.search);
  if (filters.milieu_type) params = params.set('milieu_type', filters.milieu_type);
  if (filters.type_circuit) params = params.set('type_circuit', filters.type_circuit);
  if (filters.presence_canal_amenee !== null && filters.presence_canal_amenee !== undefined) {
   params = params.set('presence_canal_amenee', String(filters.presence_canal_amenee));
  }
  return this.http.get<Centrale[]>(`${this.baseUrl}/`, {
   params,
   withCredentials: true,
  });
 }

 // ─── GET ONE ───
 getById(id: number): Observable<Centrale> {
  return this.http.get<Centrale>(`${this.baseUrl}/${id}/`, {
   withCredentials: true,
  });
 }

 // ─── CREATE ───
 create(centrale: Centrale): Observable<Centrale> {
  return this.http.post<Centrale>(`${this.baseUrl}/create/`, centrale, {
   withCredentials: true,
  });
 }

 // ─── UPDATE ───
 update(id: number, centrale: Centrale): Observable<Centrale> {
  return this.http.put<Centrale>(`${this.baseUrl}/${id}/update/`, centrale, {
   withCredentials: true,
  });
 }

 // ─── PATCH ───
 patch(id: number, partial: Partial<Centrale>): Observable<Centrale> {
  return this.http.patch<Centrale>(`${this.baseUrl}/${id}/partial/`, partial, {
   withCredentials: true,
  });
 }

 // ─── DELETE ───
 delete(id: number): Observable<void> {
  return this.http.delete<void>(`${this.baseUrl}/${id}/`, {
   withCredentials: true,
  });
 }

 // ─── EXPORT EXCEL — tous les champs ───
exportExcel(centrales: Centrale[]): void {
 const data = centrales.map(c => ({
  // Identité / Site (1.a)
  'Site': c.site_name,
  'Code': c.code_nom,
  'Milieu': c.milieu_type,
  'Source froide': c.source_froide,

  // Caractéristiques CNPE (1.b)
  'Nb réacteurs': c.nbre_reacteurs,
  'Puissance (MW)': c.puissance_reacteurs_mwe,
  'Débit aspiré par tranche (m3/s)': c.debit_aspire_par_tranche_m3s,
  'Débit total aspiré (m3/s)': c.debit_total_aspire_m3s,
  'Disponibilité tranches': c.taux_disponibilite_moyen_tranches,

  // Circuit / Filtration (1.c)
  'Type circuit': c.type_circuit,
  'Type filtration': c.type_filtration,
  'Dimension filtre (h/l/m)': c.dimension_filtre_h_l_m,
  'Maillage (mm)': c.maillage_mm,
  'Pression nettoyage': c.pression_nettoyage,
  'Traitement chimique': c.traitement_chimique ? 'Oui' : 'Non',
  'Type traitement chimique': c.type_traitement_chimique,
  'Circuits CRF/SEC séparés': c.circuits_crf_sec_separes ? 'Oui' : 'Non',
  'Pompes séparées': c.pompes_separees ? 'Oui' : 'Non',
  'Fonctionnement filtre': c.fonctionnement_filtre,
  'Temps moyen émersion (min)': c.temps_moyen_emersion_min,
  'Système récupération': c.systeme_recuperation ? 'Oui' : 'Non',
  'Présence goulotte': c.presence_goulotte ? 'Oui' : 'Non',
  'Goulotte hauteur eau (m)': c.goulotte_hauteur_eau,
  'Présence pré-grille': c.presence_pre_grille ? 'Oui' : 'Non',
  'Espacement pré-grille (mm)': c.espacement_pre_grille_mm,

  // Prise d'eau / Rejet (1.d)
  'Canal amenée': c.presence_canal_amenee ? 'Oui' : 'Non',
  'Localisation prise eau': c.localisation_prise_eau,
  'Localisation rejet eau': c.localisation_rejet_eau,
  'Profondeur rejet eau (m)': c.profondeur_rejet_eau_m,
  'Distance côte rejet eau (m)': c.distance_cote_rejet_eau_m,
  'Volume eau rejetée (m3/s)': c.volume_eau_rejetee_m3s,
  'Température rejet (°C)': c.temperature_rejet_c,
  'Température milieu (°C)': c.temperature_milieu_c,
  'Delta T (°C)': c.delta_t_c,
 }));

 this.exportService.exportToExcel(data, 'centrales', 'Centrales');
}

// ─── DOWNLOAD TEMPLATE — tous les champs ───
downloadTemplate(): void {
 const headers = [
  // Identité / Site (1.a)
  'Site',
  'Code',
  'Milieu',
  'Source froide',

  // Caractéristiques CNPE (1.b)
  'Nb réacteurs',
  'Puissance (MW)',
  'Débit aspiré par tranche (m3/s)',
  'Débit total aspiré (m3/s)',
  'Disponibilité tranches',

  // Circuit / Filtration (1.c)
  'Type circuit',
  'Type filtration',
  'Dimension filtre (h/l/m)',
  'Maillage (mm)',
  'Pression nettoyage',
  'Traitement chimique',
  'Type traitement chimique',
  'Circuits CRF/SEC séparés',
  'Pompes séparées',
  'Fonctionnement filtre',
  'Temps moyen émersion (min)',
  'Système récupération',
  'Présence goulotte',
  'Goulotte hauteur eau (m)',
  'Présence pré-grille',
  'Espacement pré-grille (mm)',

  // Prise d'eau / Rejet (1.d)
  'Canal amenée',
  'Localisation prise eau',
  'Localisation rejet eau',
  'Profondeur rejet eau (m)',
  'Distance côte rejet eau (m)',
  'Volume eau rejetée (m3/s)',
  'Température rejet (°C)',
  'Température milieu (°C)',
  'Delta T (°C)',
 ];

 this.exportService.downloadTemplate(headers, 'centrales');
}

// ─── IMPORT — mapping tous les champs ───
async importFile(file: File): Promise<Observable<ImportResult>> {
 const rows = await this.importService.readFile(file);

 const centrales: Centrale[] = rows.map((row: any) => ({
  // Identité / Site (1.a)
  site_name: row['Site'] || '',
  code_nom: row['Code'] || '',
  milieu_type: row['Milieu'] || '',
  source_froide: row['Source froide'] || '',

  // Caractéristiques CNPE (1.b)
  nbre_reacteurs: row['Nb réacteurs'] ? Number(row['Nb réacteurs']) : null,
  puissance_reacteurs_mwe: row['Puissance (MW)'] ? Number(row['Puissance (MW)']) : null,
  debit_aspire_par_tranche_m3s: row['Débit aspiré par tranche (m3/s)'] ? Number(row['Débit aspiré par tranche (m3/s)']) : null,
  debit_total_aspire_m3s: row['Débit total aspiré (m3/s)'] ? Number(row['Débit total aspiré (m3/s)']) : null,
  taux_disponibilite_moyen_tranches: row['Disponibilité tranches'] || '',

  // Circuit / Filtration (1.c)
  type_circuit: row['Type circuit'] || '',
  type_filtration: row['Type filtration'] || '',
  dimension_filtre_h_l_m: row['Dimension filtre (h/l/m)'] || '',
  maillage_mm: row['Maillage (mm)'] ? Number(row['Maillage (mm)']) : null,
  pression_nettoyage: row['Pression nettoyage'] || '',
  traitement_chimique: row['Traitement chimique'] === 'Oui',
  type_traitement_chimique: row['Type traitement chimique'] || '',
  circuits_crf_sec_separes: row['Circuits CRF/SEC séparés'] === 'Oui',
  pompes_separees: row['Pompes séparées'] === 'Oui',
  fonctionnement_filtre: row['Fonctionnement filtre'] || '',
  temps_moyen_emersion_min: row['Temps moyen émersion (min)'] ? Number(row['Temps moyen émersion (min)']) : null,
  systeme_recuperation: row['Système récupération'] === 'Oui',
  presence_goulotte: row['Présence goulotte'] === 'Oui',
  goulotte_hauteur_eau: row['Goulotte hauteur eau (m)'] ? Number(row['Goulotte hauteur eau (m)']) : null,
  presence_pre_grille: row['Présence pré-grille'] === 'Oui',
  espacement_pre_grille_mm: row['Espacement pré-grille (mm)'] ? Number(row['Espacement pré-grille (mm)']) : null,

  // Prise d'eau / Rejet (1.d)
  presence_canal_amenee: row['Canal amenée'] === 'Oui',
  localisation_prise_eau: row['Localisation prise eau'] || '',
  localisation_rejet_eau: row['Localisation rejet eau'] || '',
  profondeur_rejet_eau_m: row['Profondeur rejet eau (m)'] ? Number(row['Profondeur rejet eau (m)']) : null,
  distance_cote_rejet_eau_m: row['Distance côte rejet eau (m)'] ? Number(row['Distance côte rejet eau (m)']) : null,
  volume_eau_rejetee_m3s: row['Volume eau rejetée (m3/s)'] ? Number(row['Volume eau rejetée (m3/s)']) : null,
  temperature_rejet_c: row['Température rejet (°C)'] ? Number(row['Température rejet (°C)']) : null,
  temperature_milieu_c: row['Température milieu (°C)'] ? Number(row['Température milieu (°C)']) : null,
  delta_t_c: row['Delta T (°C)'] ? Number(row['Delta T (°C)']) : null,
 }));

 return this.importService.importRows(centrales, (c) => this.create(c));
}
}