import { Component } from '@angular/core';
import { RecService } from './recommendation.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-recommendation',
  standalone: true, // Mark as standalone
  imports: [CommonModule, FormsModule, HttpClientModule], // Add required modules
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent {
  query = '';
  results: any;

  constructor(private recService: RecService) {}

  search() {
    this.recService.getRecommendations(this.query).subscribe({
      next: (res) => {
        this.results = res;
        console.log('API response:', res);
      },
      error: (err) => {
        console.error('API error:', err);
        alert('Error fetching recommendations');
      }
    });
  }
}
