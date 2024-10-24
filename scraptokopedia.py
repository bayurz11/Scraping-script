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


# Fungsi untuk menggulir halaman ke bawah
def scroll_down(driver, times):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(random.uniform(1, 2))  # Beri jeda agar halaman sempat memuat


# Fungsi untuk mengambil data dari halaman tertentu
def get_page_data(page_number):
    retry_count = 3
    for attempt in range(retry_count):
        options = webdriver.ChromeOptions()
        # Nonaktifkan headless untuk debug
        # options.add_argument("--headless")
        driver = webdriver.Chrome(
            service=Service("chromedriver.exe"),
            options=options,
        )
        try:
            tokopedia_link = f"https://www.tokopedia.com/search?q=gundam+hg&source=universe&st=product&navsource=home&srp_component_id=02.02.02.02&page={page_number}"
            driver.set_window_size(1300, 800)
            driver.get(tokopedia_link)

            # Tunggu sampai elemen produk muncul
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-jza1fo"))
            )

            # Gulir halaman ke bawah
            scroll_down(driver, 9)

            # Ambil sumber halaman
            content = driver.page_source
            data = bs(content, "html.parser")

            # List untuk menyimpan data
            produk_data = []

            # Mengambil area produk
            for area in data.find_all("div", class_="css-5wh65g"):
                produk = {}

                # Mengambil title
                nama = area.find("span", class_="OWkG6oHwAppMn1hIBsC3pQ==")
                if nama:
                    produk["Title"] = nama.text
                else:
                    produk["Title"] = None

                # Mengambil harga
                harga = area.find("div", class_="_8cR53N0JqdRc+mQCckhS0g==")
                if harga:
                    produk["Harga"] = harga.text
                else:
                    produk["Harga"] = None

                # Mengambil harga asli (jika ada)
                harga_asli = area.find("span", class_="en+9Xhk5rmGNLiUfSuIuqg==")
                if harga_asli:
                    produk["Harga Asli"] = harga_asli.text
                else:
                    produk["Harga Asli"] = None

                # Mengambil diskon
                diskon = area.find("span", class_="_5+V0nr2fU+1eyI2rpS0FYw==")
                if diskon:
                    produk["Diskon"] = diskon.text
                else:
                    produk["Diskon"] = None

                # Mengambil jumlah terjual
                terjual = area.find("span", class_="eLOomHl6J3IWAcdRU8M08A==")
                if terjual:
                    produk["Terjual"] = terjual.text
                else:
                    produk["Terjual"] = None

                # Mengambil rating
                rating = area.find("span", class_="nBBbPk9MrELbIUbobepKbQ==")
                if rating:
                    produk["Rating"] = rating.text
                else:
                    produk["Rating"] = None

                # Mengambil lokasi
                lokasi = area.find("span", class_="-9tiTbQgmU1vCjykywQqvA== flip")
                if lokasi:
                    produk["Lokasi"] = lokasi.text
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
jumlah_halaman = 2  # Jumlah halaman yang ingin di-scrape
all_produk_data = []

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(get_page_data, page) for page in range(1, jumlah_halaman + 1)
    ]
    for future in as_completed(futures):
        all_produk_data.extend(future.result())

# Membuat DataFrame dari list produk_data
df = pd.DataFrame(all_produk_data)

# Mengekspor DataFrame ke file CSV
df.to_csv("tokopedia_data.csv", index=False, encoding="utf-8-sig")

print("Data berhasil diekspor ke tokopedia_data.csv")
