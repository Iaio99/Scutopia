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
        publications.forEach(
          publication => (
            this.publications.push(
              {
                eid: publication[0],
                authors: publication[1],
                eid__publication_date: publication[2],
                eid__title: publication[3],
                eid__magazine: publication[4],
                eid__volume: publication[5],
                eid__page_range: publication[6],
                eid__doi: publication[7],
                eid__download_date: publication[8],
                scopus_id__ssd: publication[9]
              } as Publication
            )
          )
        )
      });
  }  

}