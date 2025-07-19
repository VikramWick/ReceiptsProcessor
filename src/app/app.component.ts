import { Component, OnInit, QueryList, ViewChildren } from '@angular/core';
import { ApiService } from './api.service';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  @ViewChildren(BaseChartDirective) charts: QueryList<BaseChartDirective> | undefined;
  
  selectedFile: File | null = null;
  statusMessage: string = '';
  receipts: any[] = [];
  stats: any = null;
  filters = { search: '', start_date: '', end_date: '', sort_by: 'date', order: 'desc' };

  public barChartOptions: ChartConfiguration['options'] = { responsive: true, indexAxis: 'y', maintainAspectRatio: false };
  public barChartType: ChartType = 'bar';
  public barChartData = { labels: [] as string[], datasets: [{ data: [] as number[], label: 'No. of Receipts', backgroundColor: '#3498db' }]};

  public lineChartOptions: ChartConfiguration['options'] = { responsive: true, maintainAspectRatio: false };
  public lineChartType: ChartType = 'line';
  public lineChartData = { labels: [] as string[], datasets: [{ data: [] as number[], label: 'Total Spend', tension: 0.2, borderColor: '#2ecc71', backgroundColor: 'rgba(46, 204, 113, 0.2)', fill: 'origin' }]};

  constructor(private apiService: ApiService) {}

  ngOnInit() { this.loadAllData(); }
  loadAllData() { this.applyFilters(); this.apiService.getStats().subscribe(data => this.stats = data); this.loadChartData(); }

  loadChartData() {
    this.apiService.getVendorFrequency().subscribe(data => {
      this.barChartData.labels = data.map((d: any) => d.vendor);
      this.barChartData.datasets[0].data = data.map((d: any) => d.count);
      this.charts?.forEach(chart => chart.update());
    });
    this.apiService.getMonthlySpend().subscribe(data => {
      this.lineChartData.labels = data.map((d: any) => d.month);
      this.lineChartData.datasets[0].data = data.map((d: any) => d.total);
      this.charts?.forEach(chart => chart.update());
    });
  }
  
  onFileSelected(event: any): void { this.selectedFile = event.target.files[0] ?? null; }
  onUpload(): void { if (!this.selectedFile) return; this.statusMessage = 'Uploading...'; this.apiService.uploadReceipt(this.selectedFile).subscribe({ next: () => { this.statusMessage = 'Upload successful!'; this.selectedFile = null; (document.querySelector('input[type="file"]') as HTMLInputElement).value = ''; this.loadAllData(); setTimeout(() => this.statusMessage = '', 3000); }, error: (err) => { this.statusMessage = `Error: ${err.error.detail || 'Upload failed'}`; } }); }
  applyFilters(): void { this.apiService.getReceipts(this.filters).subscribe(data => { this.receipts = data; }); }
  resetFilters(): void { this.filters = { search: '', start_date: '', end_date: '', sort_by: 'date', order: 'desc' }; this.applyFilters(); }

  // --- ADD THIS NEW DELETE METHOD ---
  deleteReceipt(id: number): void {
    if (confirm('Are you sure you want to delete this receipt?')) {
      this.apiService.deleteReceipt(id).subscribe(() => {
        // On success, reload all data to refresh the UI
        this.loadAllData();
      });
    }
  }
}