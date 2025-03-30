import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class RecService {
  private apiUrl = 'http://localhost:8000'; // my FastAPI URL

  constructor(private http: HttpClient) { }

  getRecommendations(query: string) {
    return this.http.post(`${this.apiUrl}/recommend`, { text: query });
  }
}