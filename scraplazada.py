import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import WebDriverException
import random

# Ubah encoding output standar menjadi utf-8
sys.stdout.reconfigure(encoding="utf-8")


# Fungsi untuk mengambil data dari halaman tertentu
def get_page_data(page_number):
    retry_count = 3
    for attempt in range(retry_count):
        driver = webdriver.Chrome(
            service=Service("chromedriver.exe"),
            options=webdriver.ChromeOptions().add_argument("--headless"),
        )
        try:
            lazada_link = f"https://www.lazada.co.id/shop-beli-laptop-gaming/?spm=a2o4j.searchlistcategory.cate_1_2.2.46905a2bzDwF9E&page={page_number}"
            driver.set_window_size(1300, 800)
            driver.get(lazada_link)

            # Tunggu sampai elemen produk muncul
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Bm3ON"))
            )

            # Ambil sumber halaman
            content = driver.page_source
            data = bs(content, "html.parser")

            # List untuk menyimpan data
            produk_data = []

            # Mengambil area produk
            for area in data.find_all("div", class_="Bm3ON"):
                produk = {}

                # Mengambil title
                nama = area.find("div", class_="RfADt")
                if nama:
                    link = nama.find("a")
                    if link and "title" in link.attrs:
                        produk["Title"] = link["title"]
                    else:
                        produk["Title"] = None

                # Mengambil harga
                harga = area.find("span", class_="ooOxS")
                if harga:
                    produk["Harga"] = harga.text
                else:
                    produk["Harga"] = None

                # Mengambil diskon
                diskon = area.find("span", class_="IcOsH")
                if diskon:
                    produk["Diskon"] = diskon.text
                else:
                    produk["Diskon"] = None

                # Mengambil jumlah terjual
                terjual = area.find("span", class_="_1cEkb")
                if terjual:
                    produk["Terjual"] = terjual.text
                else:
                    produk["Terjual"] = None

                # Mengambil rating
                rating = area.find("span", class_="qzqFw")
                if rating:
                    produk["Rating"] = rating.text
                else:
                    produk["Rating"] = None

                # Mengambil lokasi
                lokasi = area.find("span", class_="oa6ri")
                if lokasi:
                    produk["Lokasi"] = lokasi["title"]
                else:
                    produk["Lokasi"] = None

                produk_data.append(produk)

            driver.quit()
            return produk_data
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            driver.quit()
            time.sleep(random.uniform(1, 3))
        finally:
            if driver:
                driver.quit()
    return []


# Mengambil data dari beberapa halaman secara paralel
jumlah_halaman = 5  # Jumlah halaman yang ingin di-scrape
all_produk_data = []

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(get_page_data, page) for page in range(1, jumlah_halaman + 1)
    ]
    for future in as_completed(futures):
        all_produk_data.extend(future.result())

# Membuat DataFrame dari list produk_data
df = pd.DataFrame(all_produk_data)

# Mengekspor DataFrame ke file Excel
df.to_excel("lazada_data_all_pages.xlsx", index=False)

print("Data berhasil diekspor ke lazada_data_all_pages.xlsx")
