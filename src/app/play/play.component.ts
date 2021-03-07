import {
  Component, Input, ElementRef, AfterViewInit, ViewChild
} from '@angular/core';
import { fromEvent } from 'rxjs';
import { switchMap, takeUntil, pairwise } from 'rxjs/operators'
import {HttpClient} from "@angular/common/http"
import {environment} from "src/environments/environment"
@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.css'],
  template: '<canvas #canvas></canvas>',
  styles: ['canvas { border: 1px solid #000;background:White }']
})
export class PlayComponent implements AfterViewInit {

  constructor(private http:HttpClient) { }
  @ViewChild('canvas') public canvas: ElementRef;
  className:any = null;

  @Input() public width = 384;
  @Input() public height = 384;

  private cx: CanvasRenderingContext2D;

  public ngAfterViewInit() {
    const canvasEl: HTMLCanvasElement = this.canvas.nativeElement;
    this.cx = canvasEl.getContext('2d');

    canvasEl.width = this.width;
    canvasEl.height = this.height;

    this.cx.lineWidth = 123;
    this.cx.lineCap = 'round';
    this.cx.strokeStyle = '#000';

    this.captureEvents(canvasEl);
  }
  
  private captureEvents(canvasEl: HTMLCanvasElement) {
    // this will capture all mousedown events from the canvas element
    fromEvent(canvasEl, 'mousedown')
      .pipe(
        switchMap((e) => {
          // after a mouse down, we'll record all mouse moves
          return fromEvent(canvasEl, 'mousemove')
            .pipe(
              // we'll stop (and unsubscribe) once the user releases the mouse
              // this will trigger a 'mouseup' event    
              takeUntil(fromEvent(canvasEl, 'mouseup')),
              // we'll also stop (and unsubscribe) once the mouse leaves the canvas (mouseleave event)
              takeUntil(fromEvent(canvasEl, 'mouseleave')),
              // pairwise lets us get the previous value to draw a line from
              // the previous point to the current point    
              pairwise()
            )
        })
      )
      .subscribe((res: [MouseEvent, MouseEvent]) => {
        const rect = canvasEl.getBoundingClientRect();
  
        // previous and current position with the offset
        const prevPos = {
          x: res[0].clientX - rect.left,
          y: res[0].clientY - rect.top
        };
  
        const currentPos = {
          x: res[1].clientX - rect.left,
          y: res[1].clientY - rect.top
        };
  
        // this method we'll implement soon to do the actual drawing
        this.drawOnCanvas(prevPos, currentPos);
      });
  }

  private drawOnCanvas(prevPos: { x: number, y: number }, currentPos: { x: number, y: number }) {
    if (!this.cx) { return; }

    this.cx.beginPath();

    if (prevPos) {
      this.cx.moveTo(prevPos.x, prevPos.y); // from
      this.cx.lineTo(currentPos.x, currentPos.y);
      this.cx.stroke();
    }
  }
clearCanvas(){
    this.cx.clearRect(0,0,this.width,this.height);
  }
saveImage(className){
  
  if (className===null){
    console.log('NOt Updated!')
    return;
    
  }
var canvas:HTMLCanvasElement=this.canvas.nativeElement
var date=Date.now();
var filename=className+'_'+date+'.png';
var image= canvas.toDataURL("image/png");
this.http.post(
  environment.SERVER_URL+'/upload_canvas',
  {filename,image,className},
  {responseType:'text'}
).subscribe((res:any)=>{
  console.log(res,className)
  this.clearCanvas();
})

}

cardContent=[{
  value:"Sun"
},
{value:"Flower"},
{value:"Pencil"},
{value:"Spoon"},
{value:"Tree"},
{value:"House"},{value:"Bird"},{value:"Hand"},{value:"Umbrella"},{value:"Spectacles"},


]
cardContent1=[{text:"Choose from the labels"},{text:"Draw inside the Canvas area"},{text:"Press confirm selection"}]

}
// ['Sun', 'Flower', 'Umbrella', 'Pencil', 'Spoon', 'Tree', 'Spectacles', 'House', 'Bird', 'Hand']