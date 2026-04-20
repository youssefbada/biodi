import { Injectable, inject } from '@angular/core';
import * as XLSX from 'xlsx';
import { Observable, from, forkJoin, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface ImportResult {
 total: number;
 success: number;
 errors: ImportError[];
}

export interface ImportError {
 ligne: number;
 message: string;
}

@Injectable({
 providedIn: 'root',
})
export class ImportService {

 // ─── Lire fichier Excel/CSV ───
 readFile(file: File): Promise<any[]> {
  return new Promise((resolve, reject) => {
   const reader = new FileReader();

   reader.onload = (e: any) => {
    try {
     const data = new Uint8Array(e.target.result);
     const workbook = XLSX.read(data, { type: 'array' });
     const sheetName = workbook.SheetNames[0];
     const worksheet = workbook.Sheets[sheetName];
     const rows = XLSX.utils.sheet_to_json(worksheet, { defval: null });
     resolve(rows);
    } catch (err) {
     reject('Erreur lors de la lecture du fichier');
    }
   };

   reader.onerror = () => reject('Erreur lors de la lecture du fichier');
   reader.readAsArrayBuffer(file);
  });
 }

 // ─── Validation fichier ───
 validateFile(file: File): { valid: boolean; error?: string } {
  const allowedTypes = [
   'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
   'application/vnd.ms-excel',
   'text/csv',
  ];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!allowedTypes.includes(file.type) && !file.name.endsWith('.xlsx') && !file.name.endsWith('.csv')) {
   return { valid: false, error: 'Format non supporté. Utilisez Excel (.xlsx) ou CSV.' };
  }
  if (file.size > maxSize) {
   return { valid: false, error: 'Fichier trop volumineux. Maximum 10MB.' };
  }
  return { valid: true };
 }

 // ─── Import multiple lignes avec plusieurs appels API ───
 importRows<T>(
  rows: T[],
  createFn: (row: T) => Observable<any>
 ): Observable<ImportResult> {
  if (rows.length === 0) {
   return of({ total: 0, success: 0, errors: [] });
  }

  const calls = rows.map((row, index) =>
   createFn(row).pipe(
    map(() => ({ success: true, ligne: index + 2 })),
    catchError((err) => of({
     success: false,
     ligne: index + 2,
     message: err?.error?.detail || `Erreur ligne ${index + 2}`
    }))
   )
  );

  return forkJoin(calls).pipe(
   map((results) => {
    const errors: ImportError[] = results
     .filter((r: any) => !r.success)
     .map((r: any) => ({ ligne: r.ligne, message: r.message }));

    return {
     total: rows.length,
     success: results.filter((r: any) => r.success).length,
     errors,
    };
   })
  );
 }
}