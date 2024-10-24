import pyautogui
import time
import urllib.parse
import subprocess

# Ganti '081318207954' dengan nomor telepon yang ingin Anda hubungi
local_phone_number = "081318207954"

# Ganti dengan pesan yang ingin Anda kirim
message = "Halo, ini adalah pesan otomatis."

# Encode pesan agar sesuai dengan format URL
encoded_message = urllib.parse.quote(message)

# Menghapus angka nol di depan nomor telepon lokal dan menambahkan kode negara Indonesia
phone_number = f"62{local_phone_number[1:]}"

# URL untuk membuka chat dengan pesan tertentu di WhatsApp Web
url = f"https://wa.me/{phone_number}?text={encoded_message}"

# Buka WhatsApp Desktop
subprocess.Popen(
    "C:\\path\\to\\WhatsApp.exe"
)  # Ganti dengan path ke executable WhatsApp Desktop

# Tunggu aplikasi untuk memuat
time.sleep(10)

# Buka jendela chat (anda mungkin perlu menyesuaikan koordinat atau penggunaan metode lain)
pyautogui.hotkey(
    "ctrl", "shift", "m"
)  # Misalnya, untuk membuka jendela chat baru, sesuaikan dengan shortcut Anda

# Tunggu jendela chat terbuka
time.sleep(5)

# Mengetik pesan
pyautogui.write(message)
pyautogui.press("enter")

# Tunggu beberapa detik sebelum menutup
time.sleep(5)
