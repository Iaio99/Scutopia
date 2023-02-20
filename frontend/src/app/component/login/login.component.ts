import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder, private loginService: LoginService) {

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
    this.loginService.login(this.loginFormGroup.get('username')!.value, this.loginFormGroup.get('password')!.value).subscribe(message => console.log(message));
  }

}