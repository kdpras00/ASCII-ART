# ASCII Art Converter

Project ini berisi tiga script Python untuk mengonversi gambar, video, dan webcam menjadi ASCII art.

## 📋 Fitur

### 1. Image to ASCII (`image_to_ascii.py`)

- Mengonversi file gambar (JPG, PNG, dll) menjadi ASCII art
- Menampilkan ASCII art di terminal
- **Mode berwarna** dengan ANSI escape code 
- Opsi untuk menyimpan hasil ke file teks atau HTML
- Mode sederhana tanpa header
- Support berbagai format gambar

### 2. Video to ASCII (`video_to_ascii.py`)

- Mengonversi file video menjadi video ASCII art
- Menampilkan ASCII art secara real-time di terminal
- Menyimpan hasil sebagai file video baru
- Support format video berbagai format (MP4, AVI, dll)

### 3. Webcam ASCII (`webcam_ascii.py`)

- Menampilkan webcam live dalam bentuk ASCII art
- Real-time processing tanpa menyimpan file
- Kontrol dengan tombol 'q' untuk keluar
- Smooth animation di terminal

## 🛠️ Instalasi

### 1. Install Python

Pastikan Python 3.7 atau lebih tinggi sudah terinstall di komputer Anda.

### 2. Install Dependencies

Jalankan command berikut untuk menginstall semua library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

Atau install secara manual:

```bash
pip install opencv-python numpy Pillow
```

## 📖 Cara Menggunakan

### Image to ASCII

1. **Siapkan file gambar**

   - Letakkan file gambar Anda di folder project
   - Atau gunakan path lengkap ke file gambar

2. **Jalankan script**

   ```bash
   python image_to_ascii.py foto.jpg
   ```

   Dengan lebar custom:

   ```bash
   python image_to_ascii.py foto.jpg 100
   ```

   **Mode berwarna full width (seperti TikTok!):**

   ```bash
   python image_to_ascii.py foto.jpg --full --color
   ```

   **Mode berwarna dengan lebar custom:**

   ```bash
   python image_to_ascii.py foto.jpg 150 --color
   ```

   Mode sederhana tanpa header:

   ```bash
   python image_to_ascii.py foto.jpg --simple
   ```

   Dengan opsi save ke file:

   ```bash
   python image_to_ascii.py foto.jpg 80 --save
   ```

   Save ke HTML:

   ```bash
   python image_to_ascii.py foto.jpg 80 --html
   ```

   Kombinasi mode berwarna + HTML:

   ```bash
   python image_to_ascii.py foto.jpg 100 --color --html
   ```

3. **Output**
   - ASCII art akan ditampilkan di terminal
   - Jika menggunakan `--save`, hasil akan disimpan ke file .txt
   - Jika menggunakan `--html`, hasil akan disimpan ke file .html
   - Mode `--color` memberikan efek seperti video TikTok yang berwarna

### Video to ASCII

1. **Siapkan file video**

   - Letakkan file video Anda di folder project
   - Atau gunakan path lengkap ke file video

2. **Jalankan script**

   ```bash
   python video_to_ascii.py
   ```

   Atau dengan nama file spesifik:

   ```bash
   python video_to_ascii.py my_video.mp4
   ```

3. **Output**
   - ASCII art akan ditampilkan di terminal frame by frame
   - Video output akan disimpan sebagai `ascii_output.mp4`

### Webcam ASCII

1. **Hubungkan webcam**

   - Pastikan webcam terhubung ke komputer
   - Tidak ada aplikasi lain yang menggunakan webcam

2. **Jalankan script**

   ```bash
   python webcam_ascii.py
   ```

   Atau dengan kamera spesifik:

   ```bash
   python webcam_ascii.py 0  # Kamera pertama (default)
   python webcam_ascii.py 1  # Kamera kedua
   ```

3. **Kontrol**
   - Tekan tombol 'q' untuk keluar
   - Atau tekan Ctrl+C

## 🎨 Karakter ASCII

Script menggunakan karakter berikut dari paling gelap hingga paling terang:

```
@%#*+=-:.
```

Karakter `@` mewakili piksel paling gelap, dan spasi mewakili piksel paling terang.

## ⚙️ Pengaturan

### Mengubah Lebar ASCII

Ubah parameter `ascii_width` dalam fungsi pemanggilan:

- Lebih kecil = detail lebih sedikit, processing lebih cepat
- Lebih besar = detail lebih banyak, processing lebih lambat

Contoh:

```python
show_webcam_ascii(camera_index=0, ascii_width=100)  # Lebih lebar
show_webcam_ascii(camera_index=0, ascii_width=60)   # Lebih sempit
```

### Mengubah Font Size (Video Output)

Ubah parameter `font_size` dalam fungsi `ascii_to_image()`:

```python
ascii_image = ascii_to_image(ascii_art, font_size=12)
```

## ✨ Fitur Lanjutan Image to ASCII

### Mode Berwarna Full Width (Color Mode)

Gunakan flag `--full --color` untuk menampilkan ASCII art berwarna yang mengisi terminal penuh:

```bash
python image_to_ascii.py foto.jpg --full --color
```

Mode ini memberikan efek visual yang menakjubkan seperti video TikTok yang populer!

### Mode Berwarna Custom Width

Gunakan flag `--color` dengan lebar tertentu:

```bash
python image_to_ascii.py foto.jpg 150 --color
```

### Mode Sederhana (Simple Mode)

Gunakan flag `--simple` untuk menampilkan ASCII art tanpa header dan footer:

```bash
python image_to_ascii.py foto.jpg --simple
```

Cocok untuk output yang lebih bersih atau untuk di-pipe ke program lain.

### Export ke HTML

Gunakan flag `--html` untuk menyimpan hasil sebagai file HTML yang bisa dibuka di browser:

```bash
python image_to_ascii.py foto.jpg --html
```

File HTML akan memiliki background hitam dan font monospace yang rapi.

### Kombinasi Fitur

Anda bisa menggabungkan beberapa fitur sekaligus:

```bash
# Berwarna + HTML
python image_to_ascii.py foto.jpg 100 --color --html

# Full width + HTML
python image_to_ascii.py foto.jpg --full --color --html

# Simpan ke file + HTML + sederhana
python image_to_ascii.py foto.jpg --save --html --simple
```

## 📝 Catatan Penting

1. **Performa**

   - Webcam ASCII akan berjalan lebih cepat daripada video processing
   - Video processing membutuhkan waktu lebih lama tergantung ukuran file
   - Lebar ASCII yang lebih kecil = processing lebih cepat

2. **Kompatibilitas Terminal**

   - Script ini bekerja di Windows PowerShell, Command Prompt, Linux Terminal, dan macOS Terminal
   - Pastikan terminal mendukung ANSI characters
   - **Untuk mode warna (--color):**
     - Terminal terbaik: Git Bash, Windows Terminal, atau terminal modern
     - Command Prompt/PowerShell lama mungkin tidak menampilkan warna
     - **Cara melihat warna dengan benar:** Gunakan flag `--html` untuk hasil terbaik!

3. **Font**

   - Script akan otomatis mencari font monospace seperti Courier New
   - Jika tidak ditemukan, akan menggunakan default font

4. **Video Output Quality**
   - Output video menggunakan format MP4
   - Kualitas tergantung pada ukuran font dan lebar ASCII

## 🐛 Troubleshooting

### "Tidak bisa membuka kamera"

- Pastikan webcam tidak digunakan aplikasi lain
- Coba ganti `camera_index` (0, 1, 2, dll)
- Periksa koneksi webcam

### "Tidak bisa membuka file video"

- Pastikan path file benar
- Cek format video yang didukung
- Install codec yang diperlukan jika perlu

### "Error: Harap sertakan path ke file gambar!"

- Pastikan menggunakan command: `python image_to_ascii.py nama_file.jpg`
- Cek apakah file gambar ada di folder yang benar
- Pastikan format gambar didukung (JPG, PNG, BMP, dll)

### Performa Lambat

- Kurangi lebar ASCII (misalnya: 60 atau 40)
- Kurangi resolusi video input
- Tutup aplikasi lain yang menggunakan banyak resource

### ImportError

- Install ulang dependencies: `pip install -r requirements.txt --upgrade`
- Pastikan menggunakan Python 3.7+

### Warna Tidak Muncul di Terminal (Mode --color)

- **Solusi terbaik:** Gunakan `--html` untuk melihat hasil berwarna di browser:
  ```bash
  python image_to_ascii.py foto.jpg --color --html
  ```
- Atau gunakan terminal modern seperti Git Bash atau Windows Terminal
- Command Prompt/PowerShell lama tidak mendukung true color
- Browser HTML selalu menampilkan warna dengan sempurna!

## 📚 Teknologi

- **OpenCV**: Computer vision dan video processing
- **NumPy**: Operasi array dan matriks
- **Pillow**: Image processing dan rendering

## 👨‍💻 Author

Project dibuat untuk demonstrasi konversi video/webcam ke ASCII art.

## 📄 License

Project ini bebas digunakan untuk keperluan personal dan edukasi.
