import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  files: File[] = [];
  isUploading = false;
  error = '';
  message = '';

  onFolderSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    this.files = input.files ? Array.from(input.files) : [];
    this.error = '';
    this.message = '';
  }

  async onSubmit(e: Event) {
    e.preventDefault();
    if (!this.files.length) return;

    this.isUploading = true;
    this.error = '';
    this.message = '';

    try {
      const formData = new FormData();
      this.files.forEach(f => formData.append('files', f, f.webkitRelativePath || f.name));

      const res = await fetch('/api/files/upload-folder', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || 'Upload failed.');
      this.message = data.message;
    } catch (err: any) {
      this.error = err?.message || 'Upload failed.';
    } finally {
      this.isUploading = false;
    }
  }
}
