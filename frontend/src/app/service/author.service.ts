import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Author } from '../model/author';

@Injectable({
  providedIn: 'root'
})
export class AuthorService {

  private authorsURL = '/api/authors/';

  constructor(private http: HttpClient) { }

  public getAuthors(): Observable<Author[]> {
    return this.http.get<Author[]>(this.authorsURL);
  }
}
