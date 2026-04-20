import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Echantillonnage } from '../../models/echantillonnage.model';
import * as XLSX from 'xlsx';

@Injectable({
  providedIn: 'root',
})
export class EchantillonnageService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/echantillonnages`;

  getAll(): Observable<Echantillonnage[]> {
    return this.http.get<Echantillonnage[]>(this.apiUrl, { withCredentials: true });
  }

  getById(id: number): Observable<Echantillonnage> {
    return this.http.get<Echantillonnage>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  create(data: Partial<Echantillonnage>): Observable<Echantillonnage> {
    return this.http.post<Echantillonnage>(`${this.apiUrl}/create/`, data, { withCredentials: true });
  }

  update(id: number, data: Partial<Echantillonnage>): Observable<Echantillonnage> {
    return this.http.put<Echantillonnage>(`${this.apiUrl}/${id}/update/`, data, { withCredentials: true });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}/delete/`, { withCredentials: true });
  }

  exportExcel(items: Echantillonnage[]): void {
    const rows = items.map(e => ({
      'ID':                        e.id_echantillonnage,
      'Centrale':                  e.centrale_id,
      'Date':                      e.date_echantillonnage,
      'Nb échantillonnage':        e.nombre_echantillonnage,
      'Durée (min)':               e.duree_echantillonnage_min,
      'Débris végétaux':           e.debris_vegetaux,
      'Groupe':                    e.groupe,
      'Poisson':                   e.poisson_id,
      'Non-poisson':               e.non_poisson_id,
      'Fréquence occurrence':      e.frequence_occurrence,
      'Juvéniles - Nb individus':  e.juveniles_nombre_individus,
      'Juvéniles - Poids':         e.juveniles_pois,
      'Juvéniles - Poids moyen':   e.juveniles_poids_moyen,
      'Juvéniles - Occurrence':    e.juveniles_occurence,
      'Juvéniles - %O':            e.juveniles_pct_o,
      'Juvéniles - Taille moy':    e.juveniles_taille_moy_cm,
      'Juvéniles - Survie':        e.juveniles_taux_survie,
      'Juvéniles - Mortalité':     e.juveniles_taux_mortalite,
      'Adultes - Nb individus':    e.adultes_nombre_individus,
      'Adultes - Poids':           e.adultes_poids,
      'Adultes - Poids moyen':     e.adultes_poids_moyen,
      'Adultes - Occurrence':      e.adultes_occurence,
      'Adultes - %O':              e.adultes_pct_o,
      'Adultes - Taille moy':      e.adultes_taille_moy_cm,
      'Adultes - Survie':          e.adultes_taux_survie,
      'Adultes - Mortalité':       e.adultes_taux_mortalite,
      'Totaux - Nb individus':     e.totaux_nombre_individus,
      'Totaux - Poids':            e.totaux_poids,
      'Totaux - Poids moyen':      e.totaux_poids_moyen,
      'Totaux - Occurrence':       e.totaux_occurence,
      'Totaux - %O':               e.totaux_pct_o,
      'Totaux - Taille moy':       e.totaux_taille_moy,
      'Totaux - Survie':           e.totaux_taux_survie,
      'Totaux - Mortalité':        e.totaux_taux_mortalite,
      'Sources':                   e.sources,
    }));

    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Echantillonnage');
    XLSX.writeFile(wb, 'echantillonnage.xlsx');
  }

  downloadTemplate(): void {
    const headers = [
      'Centrale', 'Date', 'Nb échantillonnage', 'Durée (min)', 'Débris végétaux',
      'Groupe', 'Poisson', 'Non-poisson', 'Fréquence occurrence',
      'Juvéniles - Nb individus', 'Juvéniles - Poids', 'Juvéniles - Poids moyen',
      'Juvéniles - Occurrence', 'Juvéniles - %O', 'Juvéniles - Taille moy',
      'Juvéniles - Survie', 'Juvéniles - Mortalité',
      'Adultes - Nb individus', 'Adultes - Poids', 'Adultes - Poids moyen',
      'Adultes - Occurrence', 'Adultes - %O', 'Adultes - Taille moy',
      'Adultes - Survie', 'Adultes - Mortalité',
      'Totaux - Nb individus', 'Totaux - Poids', 'Totaux - Poids moyen',
      'Totaux - Occurrence', 'Totaux - %O', 'Totaux - Taille moy',
      'Totaux - Survie', 'Totaux - Mortalité',
      'Sources',
    ];

    const ws = XLSX.utils.aoa_to_sheet([headers]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Template');
    XLSX.writeFile(wb, 'template_echantillonnage.xlsx');
  }

  async importFile(file: File): Promise<Observable<{ success: number; total: number; errors: any[] }>> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{ success: number; total: number; errors: any[] }>(
      `${this.apiUrl}/import`,
      formData,
      { withCredentials: true }
    );
  }
}