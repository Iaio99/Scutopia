import { Component, OnInit } from '@angular/core';
import { Publication } from 'src/app/model/publication';
import { PublicationService } from 'src/app/service/publication.service';

@Component({
  selector: 'app-publications',
  templateUrl: './publications.component.html',
  styleUrls: ['./publications.component.css']
})
export class PublicationsComponent implements OnInit {

  publications: Publication[] = [];
  displayedColumns: string[] = ['title', 'authors', 'publicationDate', 'doi'];

  constructor(private publicationService: PublicationService) {}

  ngOnInit(): void {
    this.publicationService.getPublications()
      .subscribe(publications => {
        publications.forEach(publication => this.publications.push(publication));
      });
  }  

}
