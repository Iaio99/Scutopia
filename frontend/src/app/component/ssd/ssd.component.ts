import { Component, OnInit } from '@angular/core';
import { Ssd } from 'src/app/model/ssd';
import { SsdService } from 'src/app/service/ssd.service';
@Component({
  selector: 'app-ssd',
  templateUrl: './ssd.component.html',
  styleUrls: ['./ssd.component.css']
})
export class SsdComponent {
  ssds: Ssd[] = [];
  displayedColumns: string[] = ['ssd', 'num_professors', 'scopus_id'];

  constructor(private SsdService: SsdService) {}

  ngOnInit(): void {
    this.SsdService.getSsds()
      .subscribe(ssds => {
        this.ssds = ssds;
      });
  }  

}