import { Component,Input,Output, OnInit } from '@angular/core';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  @Input() value: string | undefined;
    


  constructor() { }

  ngOnInit(): void {
  }
 

}
