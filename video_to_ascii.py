#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk mengonversi file video menjadi ASCII art
Menggunakan library opencv-python, numpy, dan Pillow
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Mengatur karakter ASCII dari paling gelap hingga paling terang
ASCII_CHARS = "@%#*+=-:. "

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


# Fungsi untuk mengonversi frame menjadi ASCII art
def frame_to_ascii(frame, width=80):
    """
    Mengonversi satu frame video menjadi teks ASCII art
    
    Args:
        frame: Frame video dalam format BGR
        width: Lebar output ASCII (jumlah karakter)
    
    Returns:
        String ASCII art dari frame
    """
    # Mengonversi frame BGR menjadi grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Mendapatkan dimensi frame
    original_height, original_width = gray_frame.shape
    
    # Menghitung tinggi ASCII berdasarkan rasio aspect
    aspect_ratio = original_height / original_width
    ascii_height = int(width * aspect_ratio * 0.55)  # * 0.55 karena karakter lebih tinggi daripada lebar
    
    # Resize frame ke dimensi ASCII yang diinginkan
    resized_frame = cv2.resize(gray_frame, (width, ascii_height))
    
    # Mengonversi setiap piksel menjadi karakter ASCII
    ascii_art = ""
    for row in resized_frame:
        for pixel in row:
            ascii_art += pixel_to_ascii(pixel)
        ascii_art += "\n"  # Baris baru setelah setiap row
    
    return ascii_art


# Fungsi untuk mengonversi ASCII art menjadi image untuk video output
def ascii_to_image(ascii_art, font_size=10):
    """
    Mengonversi ASCII art menjadi image PIL yang bisa disimpan sebagai frame video
    
    Args:
        ascii_art: String ASCII art
        font_size: Ukuran font untuk ASCII art
    
    Returns:
        PIL Image object
    """
    # Membaca ASCII art line by line
    lines = ascii_art.strip().split('\n')
    
    # Menghitung dimensi image yang dibutuhkan
    max_line_len = max(len(line) for line in lines)
    image_width = max_line_len * font_size
    image_height = len(lines) * font_size
    
    # Membuat image baru dengan background hitam
    img = Image.new('RGB', (image_width, image_height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Mencoba menggunakan font monospace (Courier New)
    try:
        # Mencari font yang tersedia di sistem
        font_paths = [
            "C:/Windows/Fonts/cour.ttf",  # Windows
            "C:/Windows/Fonts/courbd.ttf",  # Windows Bold
            "/System/Library/Fonts/Courier.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Linux
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break
        
        if font is None:
            # Fallback ke default font
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Menggambar setiap karakter ASCII
    y = 0
    for line in lines:
        # Menggambar teks dengan warna putih pada background hitam
        draw.text((0, y), line, fill='white', font=font)
        y += font_size
    
    return img


# Fungsi utama untuk memproses video
def process_video(input_path, output_path="ascii_output.mp4", ascii_width=80):
    """
    Memproses file video dan mengonversinya menjadi ASCII art
    
    Args:
        input_path: Path ke file video input
        output_path: Path ke file video output
        ascii_width: Lebar ASCII art dalam karakter
    """
    print(f"Memproses video: {input_path}")
    print(f"Output akan disimpan di: {output_path}")
    
    # Membuka video
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Tidak bisa membuka file video {input_path}")
        return
    
    # Mendapatkan properti video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"FPS: {fps}")
    print(f"Total frame: {total_frames}")
    
    # Inisialisasi list untuk menyimpan frame ASCII
    ascii_frames = []
    
    frame_count = 0
    
    # Loop untuk membaca setiap frame
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # Tidak ada frame lagi
        
        # Mengonversi frame menjadi ASCII art
        ascii_art = frame_to_ascii(frame, width=ascii_width)
        
        # Mengonversi ASCII art menjadi image
        ascii_image = ascii_to_image(ascii_art, font_size=10)
        
        # Mengonversi PIL Image menjadi numpy array
        ascii_array = np.array(ascii_image)
        
        # Mengonversi RGB menjadi BGR untuk OpenCV
        ascii_array_bgr = cv2.cvtColor(ascii_array, cv2.COLOR_RGB2BGR)
        
        ascii_frames.append(ascii_array_bgr)
        
        # Menampilkan ASCII art di terminal
        print(f"\nFrame {frame_count + 1}/{total_frames}")
        print(ascii_art)
        
        frame_count += 1
        
        # Optional: uncomment untuk delay jika terlalu cepat
        # import time
        # time.sleep(0.1)
    
    # Menutup video capture
    cap.release()
    
    if not ascii_frames:
        print("Error: Tidak ada frame yang berhasil diproses")
        return
    
    # Menyimpan video output
    print("\nMenyimpan video output...")
    height, width = ascii_frames[0].shape[:2]
    
    # Mengonversi list frames menjadi video menggunakan OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in ascii_frames:
        out.write(frame)
    
    out.release()
    
    print(f"Video berhasil disimpan: {output_path}")


# Fungsi main
def main():
    """
    Fungsi utama yang dipanggil saat script dijalankan
    """
    # Cek apakah ada argumen command line
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Default: mencari file input.mp4 di direktori saat ini
        input_file = "input.mp4"
    
    # Cek apakah file input ada
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} tidak ditemukan!")
        print("\nPenggunaan:")
        print("  python video_to_ascii.py [input_video.mp4]")
        print("\nAtau letakkan file video dengan nama 'input.mp4' di direktori ini")
        return
    
    # Memproses video
    process_video(input_file)


# Jalankan fungsi main jika script dijalankan langsung
if __name__ == "__main__":
    main()

