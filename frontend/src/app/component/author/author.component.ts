import { Component } from '@angular/core';
import { Author } from 'src/app/model/author';
import { AuthorService } from 'src/app/service/author.service';


@Component({
  selector: 'app-author',
  templateUrl: './author.component.html',
  styleUrls: ['./author.component.css']
})
export class AuthorComponent {
  authors: Author[] = [];
  displayedColumns: string[] = ['scopus_id', 'cf', 'nominative', 'registration_number', 'ssd', 'department', 'hire_date', 'role'];

  constructor(private AuthorService: AuthorService) {}

  ngOnInit(): void {
    this.AuthorService.getAuthors()
      .subscribe(authors => {
        this.authors = authors;
      });
  }  

}
