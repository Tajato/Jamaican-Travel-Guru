import { Component, ElementRef, ViewChild } from '@angular/core';
import { RecService } from './recommendation.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-recommendation',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent {
  @ViewChild('responseContainer') responseContainer!: ElementRef;
  query = '';
  results: any;
  copied = false;

  constructor(private recService: RecService) {}

  // Response did not lucky user friendly, this method formats it nicely.
  get formattedResponse(): string {
    if (!this.results?.llm_response) return '';
    
    return this.results.llm_response
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\d+\.\s+(.*?)(?=\n|$)/g, '<li>$1</li>')
      .replace(/Practical tip:/g, '<h3>Practical tip:</h3>')
      .replace(/<li>.*<\/li>/g, (match: any) => `<ul>${match}</ul>`);
  }

  // search method that calls the service to return a recommendation
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

  // This method allows for copying the response
  copyResponse() {
    const range = document.createRange();
    range.selectNode(this.responseContainer.nativeElement);
    window.getSelection()?.removeAllRanges();
    window.getSelection()?.addRange(range);
    document.execCommand('copy');
    this.copied = true;
    
    setTimeout(() => this.copied = false, 2000);
  }
}