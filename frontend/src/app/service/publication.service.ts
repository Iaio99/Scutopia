import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Publication } from '../model/publication';

@Injectable({
  providedIn: 'root'
})
export class PublicationService {

  private publicationsURL = '//localhost:8000/api/publications/';

  constructor(private http: HttpClient) { }

  public getPublications(): Observable<Array<Array<any>>> {
    console.info("Retrieving data...");
    return this.http.get<Array<Array<any>>>(this.publicationsURL);
  }
}
