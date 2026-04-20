import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { NonPoisson } from '../../models/non-poisson.model';
import * as XLSX from 'xlsx';

@Injectable({
  providedIn: 'root',
})
export class NonPoissonsService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/non-poissons`;

  getAll(): Observable<NonPoisson[]> {
    return this.http.get<NonPoisson[]>(this.apiUrl, { withCredentials: true });
  }

  getById(id: number): Observable<NonPoisson> {
    return this.http.get<NonPoisson>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  create(data: Partial<NonPoisson>): Observable<NonPoisson> {
    return this.http.post<NonPoisson>(this.apiUrl, data, { withCredentials: true });
  }

  update(id: number, data: Partial<NonPoisson>): Observable<NonPoisson> {
    return this.http.put<NonPoisson>(`${this.apiUrl}/${id}`, data, { withCredentials: true });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  exportExcel(items: NonPoisson[]): void {
    const rows = items.map(p => ({
      'Groupe':                    p.groupe,
      'Famille':                   p.famille,
      'Genre':                     p.genre,
      'Espèce':                    p.espece,
      'Nom commun':                p.nom_commun,
      'Guilde écologique':         p.guilde_ecologique,
      'Répartition colonne eau':   p.repartition_colonne_eau,
      'Guilde trophique':          p.guilde_trophique,
      'Enjeu halieutique':         p.enjeu_halieutique,
      'État stock':                p.etat_stock,
      'Statut protection':         p.statut_protection,
      'Conservation FR':           p.conservation_fr,
      'Conservation EU':           p.conservation_eu,
      'Conservation MD':           p.conservation_md,
      'Sensibilité lumière':       p.sensibilite_lumiere,
      'Sensibilité courant':       p.sensibilite_courants_eau,
      'Sensibilité sonore':        p.sensibilite_sonore,
      'Résistance mécanique':      p.resistance_chocs_mecaniques,
      'Résistance chimique':       p.resistance_chocs_chimiques,
      'Résistance thermique':      p.resistance_chocs_thermiques,
      'Endurance':                 p.endurance,
      'Vitesse nage min (m/s)':    p.vitesse_nage_min_ms,
      'Vitesse nage moy (m/s)':    p.vitesse_nage_moy_ms,
      'Vitesse nage max (m/s)':    p.vitesse_nage_max_ms,
    }));

    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Non-poissons');
    XLSX.writeFile(wb, 'non-poissons.xlsx');
  }

  downloadTemplate(): void {
    const headers = [
      'Groupe', 'Famille', 'Genre', 'Espèce', 'Nom commun',
      'Guilde écologique', 'Répartition colonne eau', 'Guilde trophique',
      'Enjeu halieutique', 'État stock', 'Statut protection',
      'Conservation FR', 'Conservation EU', 'Conservation MD',
      'Sensibilité lumière', 'Sensibilité courant', 'Sensibilité sonore',
      'Résistance mécanique', 'Résistance chimique', 'Résistance thermique',
      'Endurance',
      'Vitesse nage min (m/s)', 'Vitesse nage moy (m/s)', 'Vitesse nage max (m/s)',
    ];

    const ws = XLSX.utils.aoa_to_sheet([headers]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Template');
    XLSX.writeFile(wb, 'template_non_poissons.xlsx');
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