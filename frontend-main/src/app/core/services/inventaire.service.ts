import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Inventaire } from '../../models/inventaire.model';
import * as XLSX from 'xlsx';

@Injectable({
  providedIn: 'root',
})
export class InventaireService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/inventaires-milieu`;

  getAll(): Observable<Inventaire[]> {
    return this.http.get<Inventaire[]>(this.apiUrl, { withCredentials: true });
  }

  getById(id: number): Observable<Inventaire> {
    return this.http.get<Inventaire>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  create(data: Partial<Inventaire>): Observable<Inventaire> {
    return this.http.post<Inventaire>(`${this.apiUrl}/create/`, data, { withCredentials: true });
  }

  update(id: number, data: Partial<Inventaire>): Observable<Inventaire> {
    return this.http.put<Inventaire>(`${this.apiUrl}/${id}`, data, { withCredentials: true });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  exportExcel(items: Inventaire[]): void {
    const rows = items.map(i => ({
      'Centrale':              i.centrale_label,
      'Nom commun':            i.nom_commun,
      'Groupe poisson':        i.groupe_poisson,
      'Groupe non-poisson':    i.groupe_non_poisson,
      'Espèce poisson':        i.espece_poisson_label,
      'Espèce non-poisson':    i.espece_non_poisson_label,
    }));

    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Inventaire');
    XLSX.writeFile(wb, 'inventaire.xlsx');
  }

  downloadTemplate(): void {
    const headers = [
      'Centrale', 'Nom commun',
      'Groupe poisson', 'Espèce poisson',
      'Groupe non-poisson', 'Espèce non-poisson',
    ];
    const ws = XLSX.utils.aoa_to_sheet([headers]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Template');
    XLSX.writeFile(wb, 'template_inventaire.xlsx');
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