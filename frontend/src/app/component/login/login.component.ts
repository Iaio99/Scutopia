import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private router: Router) {

    this.loginFormGroup = this.formBuilder.nonNullable.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
    });
  }

  ngOnInit() {
    
  }

  public login() {
    console.log(this.loginFormGroup.value);
    
    this.loginFormGroup.reset();
    this.loginService.login(
      this.loginFormGroup.get('username')!.value,
      this.loginFormGroup.get('password')!.value)
    .subscribe({
      next: () => this.router.navigate(['publications']),
      error: () => alert('Error al Conectar Datos ')
  });
  }

}