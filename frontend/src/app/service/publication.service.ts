import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Publication } from '../model/publication';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PublicationService {

  private publicationsURL = 'https://localhost:8000/publications/';

  constructor(private http: HttpClient) { }

  public getPublications(): Observable<Publication[]> {
    return this.http.get<Publication[]>(this.publicationsURL);
  }
}