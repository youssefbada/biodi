import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Poisson } from '../../models/poisson.model';
import * as XLSX from 'xlsx';

export interface PoissonFilters {
  search?: string;
  guilde_ecologique?: string;
  repartition_colonne_eau?: string;
  guilde_trophique?: string;
}

@Injectable({
  providedIn: 'root',
})
export class PoissonsService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/poissons`;

  getAll(): Observable<Poisson[]> {
    return this.http.get<Poisson[]>(this.apiUrl, { withCredentials: true });
  }

  getById(id: number): Observable<Poisson> {
    return this.http.get<Poisson>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  create(data: Partial<Poisson>): Observable<Poisson> {
    return this.http.post<Poisson>(this.apiUrl, data, { withCredentials: true });
  }

  update(id: number, data: Partial<Poisson>): Observable<Poisson> {
    return this.http.put<Poisson>(`${this.apiUrl}/${id}`, data, { withCredentials: true });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { withCredentials: true });
  }

  exportExcel(poissons: Poisson[]): void {
    const rows = poissons.map(p => ({
      'Famille': p.famille,
      'Genre': p.genre,
      'Espèce': p.espece,
      'Nom commun': p.nom_commun,
      'Guilde écologique': p.guilde_ecologique,
      'Répartition colonne eau': p.repartition_colonne_eau,
      'Guilde trophique': p.guilde_trophique,
      'Intérêt halieutique': p.interet_halieutique,
      'État stock': p.etat_stock,
      'Statut protection': p.statut_protection,
      'Conservation FR': p.conservation_fr,
      'Conservation EU': p.conservation_eu,
      'Conservation MD': p.conservation_md,
      'Sensibilité lumière': p.sensibilite_lumiere,
      'Sensibilité courant': p.sensibilite_courants_eau,
      'Sensibilité sonore': p.sensibilite_sonore,
      'Résistance mécanique': p.resistance_chocs_mecaniques,
      'Résistance chimique': p.resistance_chocs_chimiques,
      'Résistance thermique': p.resistance_chocs_thermiques,
      'Comportement': p.comportement,
      'Période reproduction': p.periode_reproduction,
      'Forme corps': p.forme_corps,
      'Type peau': p.type_peau,
      'Locomotion': p.locomotion,
      'Endurance': p.endurance,
      'Vitesse croisière juvenile (m/s)': p.vitesse_croisiere_juvenile_ms,
      'Vitesse soutenue juvenile (m/s)': p.vitesse_soutenue_juvenile_ms,
      'Vitesse sprint juvenile (m/s)': p.vitesse_sprint_juvenile_ms,
      'Vitesse croisière adulte (m/s)': p.vitesse_croisiere_adulte_ms,
      'Vitesse soutenue adulte (m/s)': p.vitesse_soutenue_adulte_ms,
      'Vitesse sprint adulte (m/s)': p.vitesse_sprint_adulte_ms,
    }));

    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Poissons');
    XLSX.writeFile(wb, 'poissons.xlsx');
  }

  downloadTemplate(): void {
    const headers = [
      'Famille', 'Genre', 'Espèce', 'Nom commun',
      'Guilde écologique', 'Répartition colonne eau', 'Guilde trophique',
      'Intérêt halieutique', 'État stock', 'Statut protection',
      'Conservation FR', 'Conservation EU', 'Conservation MD',
      'Sensibilité lumière', 'Sensibilité courant', 'Sensibilité sonore',
      'Résistance mécanique', 'Résistance chimique', 'Résistance thermique',
      'Comportement', 'Période reproduction', 'Forme corps', 'Type peau',
      'Locomotion', 'Endurance',
      'Vitesse croisière juvenile (m/s)', 'Vitesse soutenue juvenile (m/s)', 'Vitesse sprint juvenile (m/s)',
      'Vitesse croisière adulte (m/s)', 'Vitesse soutenue adulte (m/s)', 'Vitesse sprint adulte (m/s)',
    ];

    const ws = XLSX.utils.aoa_to_sheet([headers]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Template');
    XLSX.writeFile(wb, 'template_poissons.xlsx');
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