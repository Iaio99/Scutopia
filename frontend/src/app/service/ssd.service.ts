import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Ssd } from '../model/ssd';

@Injectable({
  providedIn: 'root'
})


export class SsdService {

  private ssdsURL = '//5.75.147.58/api/ssd/';

  constructor(private http: HttpClient) { }

  public getSsds(): Observable<Ssd[]> {
    return this.http.get<Ssd[]>(this.ssdsURL);
  }
}