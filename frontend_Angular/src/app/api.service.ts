import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  uploadReceipt(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(`${this.apiUrl}/upload/`, formData);
  }

  getReceipts(filters: any): Observable<any[]> {
    let params = new HttpParams();
    for (const key in filters) {
      if (filters[key]) {
        params = params.set(key, filters[key]);
      }
    }
    return this.http.get<any[]>(`${this.apiUrl}/receipts/`, { params });
  }

  getStats(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/receipts/stats/`);
  }

  getVendorFrequency(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/receipts/stats/vendor-frequency/`);
  }

  getMonthlySpend(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/receipts/stats/monthly-spend/`);
  }

  deleteReceipt(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/receipts/${id}`);
  }
}