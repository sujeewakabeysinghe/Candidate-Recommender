import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  fileName = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event : any) {
      const file:File = event.target.files[0];
      if (file) {
          this.fileName = file.name;
          const formData = new FormData();
          formData.append("thumbnail", file);
          console.log(file)
          const upload$ = this.http.post("http://localhost:3000/resume/upload", formData);
          upload$.subscribe(res =>{
            console.log(res)
          });
      }
  }
}
