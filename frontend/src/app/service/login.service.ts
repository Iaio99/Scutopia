import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginComponent } from '../component/login/login.component';
import { LoginMessage } from '../login-message';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private loginURL = "https://5.75.147.58/api/accounts/login/";

  constructor(private http: HttpClient) { }

  public login(username: string, password: string): Observable<any>  {
    return this.http.post(this.loginURL, {"username": username, "password": password})
//    {"message": "Login Successfull!"}
  }
}
