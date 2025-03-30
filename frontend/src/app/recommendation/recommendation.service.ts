import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.prod';
import { delay, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RecService {
  private apiUrl = environment.apiUrl; // backend url link

  constructor(private http: HttpClient) { }

  // calls the fastAPI backend
  getRecommendations(query: string) {
    return this.http.post(`${this.apiUrl}/recommend`, { text: query }).pipe(retry(3), delay(1000));
  }
}