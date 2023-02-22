import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthorComponent } from './component/author/author.component';
import { LoginComponent } from './component/login/login.component';
import { PublicationComponent } from './component/publication/publication.component';
import { SsdComponent } from './component/ssd/ssd.component';


const routes: Routes = [
  {
    path: '', redirectTo: '/login', pathMatch: 'full'
  },
  {
    path: 'login', component: LoginComponent
  },
  {
    path: 'publications', component: PublicationComponent
  },
  {
    path: 'ssd', component: SsdComponent
  },
  {
    path: 'author', component: AuthorComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }