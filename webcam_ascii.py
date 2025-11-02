#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk menampilkan kamera webcam secara real-time dalam bentuk ASCII art
Menggunakan library opencv-python dan numpy
"""

import cv2
import numpy as np
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


# Fungsi untuk clear terminal (cross-platform)
def clear_terminal():
    """
    Membersihkan terminal untuk membuat tampilan lebih smooth
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Fungsi utama untuk menampilkan webcam ASCII
def show_webcam_ascii(camera_index=0, ascii_width=80):
    """
    Menampilkan webcam secara real-time dalam bentuk ASCII art
    
    Args:
        camera_index: Index kamera yang digunakan (default: 0)
        ascii_width: Lebar ASCII art dalam karakter (default: 80)
    """
    print(f"Membuka kamera {camera_index}...")
    
    # Membuka webcam
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Error: Tidak bisa membuka kamera {camera_index}")
        print("Pastikan webcam terhubung dan tidak digunakan aplikasi lain")
        return
    
    # Mengatur resolusi kamera (opsional, untuk performa lebih baik)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\nWebcam berhasil dibuka!")
    print("Tekan 'q' untuk keluar")
    print("-" * 50)
    
    # Variabel untuk kontrol
    frame_count = 0
    
    try:
        # Loop untuk membaca frame dari webcam
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Tidak bisa membaca frame dari kamera")
                break
            
            # Mengonversi frame menjadi ASCII art
            ascii_art = frame_to_ascii(frame, width=ascii_width)
            
            # Membersihkan terminal sebelum menampilkan frame baru
            # (uncomment jika ingin smooth animation, tapi bisa membuat terminal berkedip)
            # clear_terminal()
            
            # Menampilkan ASCII art di terminal
            print(f"Frame {frame_count + 1} | Tekan 'q' untuk keluar")
            print(ascii_art)
            print("-" * 50)
            
            frame_count += 1
            
            # Cek jika user menekan tombol 'q' (polling dengan timeout pendek)
            # Catatan: Ini hanya bekerja jika terminal/window aktif
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nKeluar dari aplikasi...")
                break
            
            # Optional: delay kecil untuk mengurangi beban CPU
            # Uncomment jika framerate terlalu tinggi
            # import time
            # time.sleep(0.03)  # ~30 fps
    
    except KeyboardInterrupt:
        print("\n\nMenghentikan aplikasi...")
    
    finally:
        # Tutup kamera
        cap.release()
        cv2.destroyAllWindows()
        print("Kamera ditutup. Terima kasih!")


# Fungsi main
def main():
    """
    Fungsi utama yang dipanggil saat script dijalankan
    """
    # Cek apakah ada argumen command line untuk camera index
    camera_index = 0  # Default: webcam pertama
    ascii_width = 80  # Default: lebar ASCII
    
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print(f"Error: '{sys.argv[1]}' bukan angka yang valid")
            print("\nPenggunaan:")
            print("  python webcam_ascii.py [camera_index]")
            print("\nContoh:")
            print("  python webcam_ascii.py 0    # Menggunakan kamera pertama (default)")
            print("  python webcam_ascii.py 1    # Menggunakan kamera kedua")
            return
    
    if len(sys.argv) > 2:
        try:
            ascii_width = int(sys.argv[2])
        except ValueError:
            print(f"Error: '{sys.argv[2]}' bukan angka yang valid")
            print("\nPenggunaan:")
            print("  python webcam_ascii.py [camera_index] [width]")
            return
    
    # Menampilkan webcam ASCII
    show_webcam_ascii(camera_index, ascii_width)


# Jalankan fungsi main jika script dijalankan langsung
if __name__ == "__main__":
    main()

