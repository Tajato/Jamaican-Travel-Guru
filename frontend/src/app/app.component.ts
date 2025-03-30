import { Component } from '@angular/core';
import { RecommendationComponent } from './recommendation/recommendation.component';

@Component({
  selector: 'app-root',
  imports: [RecommendationComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
}
