#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk mengonversi file gambar menjadi ASCII art
Menggunakan library Pillow dan numpy
"""

import numpy as np
from PIL import Image
import os
import sys
import shutil

# Mengatur karakter ASCII dari paling gelap hingga paling terang
ASCII_CHARS = "@%#*+=-:. "

# Fungsi untuk mendapatkan lebar terminal
def get_terminal_width():
    """
    Mendapatkan lebar terminal saat ini
    
    Returns:
        Lebar terminal dalam kolom (default: 80 jika tidak bisa dideteksi)
    """
    try:
        # Coba menggunakan shutil untuk mendapatkan terminal size (Python 3.3+)
        terminal_size = shutil.get_terminal_size()
        return terminal_size.columns
    except:
        try:
            # Fallback: coba menggunakan environment variable
            if 'COLUMNS' in os.environ:
                return int(os.environ['COLUMNS'])
            # Default width
            return 80
        except:
            return 80

# Fungsi untuk mengonversi piksel grayscale menjadi karakter ASCII
def pixel_to_ascii(pixel_value):
    """
    Mengonversi nilai piksel (0-255) menjadi karakter ASCII yang sesuai
    Nilai lebih gelap -> karakter lebih "tebal" seperti @
    Nilai lebih terang -> karakter lebih "tipis" seperti spasi
    """
    # Menyesuaikan nilai piksel ke indeks karakter ASCII
    ascii_index = int(pixel_value * (len(ASCII_CHARS) - 1) / 255)
    return ASCII_CHARS[ascii_index]


# Fungsi untuk mengonversi gambar menjadi ASCII art
def image_to_ascii(image_path, width=80, use_color=False):
    """
    Mengonversi file gambar menjadi teks ASCII art
    
    Args:
        image_path: Path ke file gambar
        width: Lebar output ASCII (jumlah karakter)
        use_color: Apakah ingin menggunakan warna (RGB)
    
    Returns:
        String ASCII art dari gambar
    """
    try:
        # Membuka gambar menggunakan Pillow
        image = Image.open(image_path)
        
        # Mendapatkan dimensi gambar
        original_width, original_height = image.size
        
        # Menghitung tinggi ASCII berdasarkan rasio aspect
        aspect_ratio = original_height / original_width
        ascii_height = int(width * aspect_ratio * 0.55)  # * 0.55 karena karakter lebih tinggi daripada lebar
        
        # Mengonversi gambar menjadi ASCII art dengan warna atau grayscale
        if use_color:
            # Versi berwarna dengan ANSI escape code
            rgb_image = image.convert('RGB')
            rgb_pixels = np.array(rgb_image.resize((width, ascii_height)))
            
            # Juga resize untuk grayscale untuk karakter ASCII
            gray_image = image.convert('L')
            gray_pixels = np.array(gray_image.resize((width, ascii_height)))
            
            ascii_art = ""
            for y in range(ascii_height):
                for x in range(width):
                    r, g, b = rgb_pixels[y, x]
                    pixel_value = gray_pixels[y, x]
                    char = pixel_to_ascii(pixel_value)
                    # Menggunakan ANSI escape code untuk RGB color
                    ascii_art += f"\033[38;2;{r};{g};{b}m{char}"
                ascii_art += "\033[0m\n"  # Reset color setelah setiap baris
        else:
            # Versi grayscale biasa
            gray_image = image.convert('L')
            resized_image = gray_image.resize((width, ascii_height))
            pixels = np.array(resized_image)
            
            ascii_art = ""
            for row in pixels:
                for pixel in row:
                    ascii_art += pixel_to_ascii(pixel)
                ascii_art += "\n"  # Baris baru setelah setiap row
        
        return ascii_art
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


# Fungsi untuk menyimpan ASCII art ke file teks
def save_ascii_to_file(ascii_art, output_path):
    """
    Menyimpan ASCII art ke file teks
    
    Args:
        ascii_art: String ASCII art
        output_path: Path untuk file output
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ascii_art)
        print(f"ASCII art berhasil disimpan ke: {output_path}")
    except Exception as e:
        print(f"Error saat menyimpan file: {str(e)}")


# Fungsi untuk mengonversi ANSI escape codes ke HTML span dengan inline styles
def convert_ansi_to_html(ascii_art):
    """
    Mengonversi ASCII art dengan ANSI escape codes menjadi HTML dengan span berwarna
    
    Args:
        ascii_art: String ASCII art dengan ANSI escape codes
    
    Returns:
        String HTML dengan span tags untuk warna
    """
    import re
    
    lines = ascii_art.split('\n')
    html_lines = []
    
    # Pattern untuk ANSI escape codes: \033[38;2;R;G;Bm
    ansi_pattern = re.compile(r'\033\[38;2;(\d+);(\d+);(\d+)m(.?)\033\[0m')
    
    for line in lines:
        # Split line into segments (ANSI codes + characters)
        html_line = '<span>'
        remaining = line
        
        while remaining:
            # Cari ANSI color codes
            match = re.search(r'\033\[38;2;(\d+);(\d+);(\d+)m', remaining)
            
            if match:
                # Tulis bagian sebelum match
                before = remaining[:match.start()]
                if before:
                    html_line += before
                
                # Tulis span dengan warna
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                html_line += f'</span><span style="color: rgb({r},{g},{b});">'
                
                # Cari end marker (\033[0m atau sampai ANSI code berikutnya)
                end_match = re.search(r'\033\[0m', remaining[match.end():])
                if end_match:
                    # Tulis char antar match dan end
                    html_line += remaining[match.end():match.end()+end_match.start()]
                    html_line += '</span><span>'
                    remaining = remaining[match.end()+end_match.end():]
                else:
                    # Tidak ada end marker, tulis sampai akhir atau sampai ANSI code berikutnya
                    next_match = re.search(r'\033\[38;2;\d+;\d+;\d+m', remaining[match.end():])
                    if next_match:
                        html_line += remaining[match.end():match.end()+next_match.start()]
                        remaining = remaining[match.end()+next_match.start():]
                    else:
                        html_line += remaining[match.end():]
                        remaining = ''
            else:
                # Tidak ada ANSI codes lagi
                html_line += remaining
                remaining = ''
        
        html_line += '</span>'
        html_lines.append(html_line)
    
    return '<br>\n'.join(html_lines)


# Fungsi untuk menyimpan ASCII art ke file HTML (dengan warna)
def save_ascii_to_html(ascii_art, output_path):
    """
    Menyimpan ASCII art ke file HTML
    
    Args:
        ascii_art: String ASCII art (dengan atau tanpa ANSI escape codes)
        output_path: Path untuk file output HTML
    """
    try:
        # Jika ada ANSI escape codes, konversi ke HTML dengan span
        if '\033[' in ascii_art:
            # Konversi ANSI ke HTML dengan span berwarna
            html_content = convert_ansi_to_html(ascii_art)
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>ASCII Art</title>
    <style>
        body {{
            background: black;
            color: white;
            font-family: 'Consolas', 'Courier New', monospace;
            white-space: pre;
            margin: 20px;
            line-height: 1;
        }}
        span {{
            color: white;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        else:
            # Grayscale, normal HTML
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>ASCII Art</title>
    <style>
        body {{
            background: black;
            color: white;
            font-family: 'Consolas', 'Courier New', monospace;
            white-space: pre;
            margin: 20px;
            line-height: 1;
        }}
    </style>
</head>
<body>
<pre>{ascii_art}</pre>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"ASCII art disimpan ke HTML: {output_path}")
    except Exception as e:
        print(f"Error saat menyimpan file HTML: {str(e)}")


# Fungsi untuk mengonversi gambar menjadi ASCII art dengan pilihan output
def convert_image(image_path, width=80, save_to_file=False, output_path=None, 
                  use_color=False, simple_mode=False, save_html=False):
    """
    Fungsi utama untuk mengonversi gambar menjadi ASCII art
    
    Args:
        image_path: Path ke file gambar
        width: Lebar ASCII art dalam karakter
        save_to_file: Apakah ingin menyimpan ke file
        output_path: Path untuk file output (opsional)
        use_color: Apakah menggunakan mode warna
        simple_mode: Mode sederhana tanpa header
        save_html: Apakah menyimpan ke HTML
    """
    if not simple_mode:
        print(f"Mengonversi gambar: {image_path}")
        print(f"Lebar ASCII: {width} karakter")
        if use_color:
            print("Mode: Berwarna (Color)")
    
    # Mengonversi gambar menjadi ASCII art
    ascii_art = image_to_ascii(image_path, width, use_color)
    
    if ascii_art is None:
        print("Gagal mengonversi gambar")
        return
    
    # Menampilkan ASCII art di terminal
    if not simple_mode:
        print("\n" + "="*60)
        print("HASIL ASCII ART:")
        print("="*60)
    print(ascii_art)
    if not simple_mode:
        print("="*60)
    
    # Menyimpan ke file jika diminta
    if save_to_file:
        if output_path is None:
            # Generate output path dari input path
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base_name}_ascii.txt"
        
        save_ascii_to_file(ascii_art, output_path)
    
    # Menyimpan ke HTML jika diminta
    if save_html:
        if output_path and output_path.endswith('.html'):
            html_output = output_path
        else:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            html_output = f"{base_name}_ascii.html"
        
        save_ascii_to_html(ascii_art, html_output)


# Fungsi main
def main():
    """
    Fungsi utama yang dipanggil saat script dijalankan
    """
    # Cek apakah ada argumen command line
    if len(sys.argv) < 2:
        print("Error: Harap sertakan path ke file gambar!")
        print("\nPenggunaan:")
        print("  python image_to_ascii.py <gambar.jpg> [lebar] [--full] [--color] [--simple] [--save] [--html] [--output file.txt]")
        print("\nContoh:")
        print("  python image_to_ascii.py foto.jpg")
        print("  python image_to_ascii.py foto.jpg 100")
        print("  python image_to_ascii.py foto.jpg --full --color")
        print("  python image_to_ascii.py foto.jpg 80 --color")
        print("  python image_to_ascii.py foto.jpg 80 --save")
        print("  python image_to_ascii.py foto.jpg 100 --save --output hasil.txt")
        print("  python image_to_ascii.py foto.jpg 80 --color --html")
        print("  python image_to_ascii.py foto.jpg --simple")
        return
    
    input_file = sys.argv[1]
    
    # Cek apakah file input ada
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} tidak ditemukan!")
        return
    
    # Parse argumen tambahan
    width = 80  # Default lebar
    save_to_file = False
    output_path = None
    use_color = False
    simple_mode = False
    save_html = False
    use_full_width = False
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        # Cek apakah ini adalah angka (lebar ASCII)
        if arg.isdigit():
            width = int(arg)
        # Cek apakah ini adalah flag --save
        elif arg == '--save':
            save_to_file = True
        # Cek apakah ini adalah flag --output
        elif arg == '--output' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 1
        # Cek apakah ini adalah flag --color
        elif arg == '--color':
            use_color = True
        # Cek apakah ini adalah flag --simple
        elif arg == '--simple':
            simple_mode = True
        # Cek apakah ini adalah flag --html
        elif arg == '--html':
            save_html = True
        # Cek apakah ini adalah flag --full
        elif arg == '--full':
            use_full_width = True
        
        i += 1
    
    # Jika --full digunakan, set width ke lebar terminal
    if use_full_width:
        terminal_w = get_terminal_width()
        # Gunakan penuh lebar terminal (jika save ke file, kurangi sedikit)
        if save_to_file or save_html:
            width = max(40, terminal_w - 20)
        else:
            # Untuk output ke terminal, gunakan penuh
            width = max(40, terminal_w)
    
    # Konversi gambar
    convert_image(input_file, width, save_to_file, output_path, use_color, simple_mode, save_html)


# Jalankan fungsi main jika script dijalankan langsung
if __name__ == "__main__":
    main()

