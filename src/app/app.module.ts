import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; // <-- Import FormsModule
import { NgChartsModule } from 'ng2-charts'; // <-- Import NgChartsModule

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,      
    NgChartsModule    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }