import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private loginURL = "http://localhost:8000/accounts/login/";

  constructor(private http: HttpClient) { }

  public login(username: string, password: string) {

  }
}