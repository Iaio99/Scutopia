import { Component, OnInit } from '@angular/core';
import { Publication } from 'src/app/model/publication';
import { PublicationService } from 'src/app/service/publication.service';

@Component({
  selector: 'app-publication',
  templateUrl: './publication.component.html',
  styleUrls: ['./publication.component.css']
})
export class PublicationComponent implements OnInit {

  publications: Publication[] = [];
  displayedColumns: string[] = ['title', 'authors', 'publication_date', 'doi'];

  constructor(private publicationService: PublicationService) {}

  ngOnInit(): void {
    this.publicationService.getPublications()
      .subscribe(publications => {
        this.publications = publications;
      });
      console.log(this.publications);
  }  

}