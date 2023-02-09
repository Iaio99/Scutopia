import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Publication } from '../model/publication';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PublicationService {

  private publicationsURL = 'localhost:8080/publications';

  constructor(private http: HttpClient) { }

  public getPublications() {
    // TODO manage service. This is only stub.

    let x = [{
      eid: 'prova',
      title: "Prova pubblicazione",
      authors: [
       {
          id: 1,
          firstName: "Andrea",
          lastName: "Cantarini",
          department: "Ingegneria"
       }
      ],
      magazine: 'tor vergogna',
      volume: 3,
      pageRange: {
        start: 1,
        end: 2
      },
      publicationDate: 'today',
      doi: "https://www.google.com",
      dateGot: new Date(),
      scopusID: 'abc'
     },
     {
      eid: 'prova',
      title: "Prova pubblicazione 2",
      authors: [
       {
          id: 1,
          firstName: "Giuliano",
          lastName: "Vallone",
          department: "Ingegneria"
       }
      ],
      magazine: 'tor vergogna',
      volume: 3,
      pageRange: {
        start: 1,
        end: 2
      },
      publicationDate: 'today',
      doi: "https://www.google.com",
      dateGot: new Date(),
      scopusID: 'abc'
     },
     {
      eid: 'prova',
      title: "Prova pubblicazione 3",
      authors: [
       {
          id: 1,
          firstName: "Valerio",
          lastName: "Mazza",
          department: "Ingegneria"
       }
      ],
      magazine: 'tor vergogna',
      volume: 3,
      pageRange: {
        start: 1,
        end: 2
      },
      publicationDate: 'today',
      doi: "https://www.google.com",
      dateGot: new Date(),
      scopusID: 'abc'
     },
    ];

    return of(x);
  }
}
