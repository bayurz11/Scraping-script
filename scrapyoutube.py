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
def get_page_data():
    retry_count = 3
    for attempt in range(retry_count):
        driver = webdriver.Chrome(
            service=Service("chromedriver.exe"),
            options=webdriver.ChromeOptions().add_argument("--headless"),
        )
        try:
            youtube_link = "https://www.youtube.com/results?search_query=laravel"
            driver.set_window_size(1300, 800)
            driver.get(youtube_link)

            # Tunggu sampai elemen video muncul
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "video-title"))
            )

            # List untuk menyimpan data
            video_data = []

            # Scroll ke bawah beberapa kali untuk memuat lebih banyak video
            scroll_count = 10
            for _ in range(scroll_count):
                driver.execute_script(
                    "window.scrollTo(0, document.documentElement.scrollHeight);"
                )
                time.sleep(
                    random.uniform(2, 4)
                )  # Tunggu beberapa detik untuk memuat konten

            # Ambil sumber halaman
            content = driver.page_source
            data = bs(content, "html.parser")

            # Mengambil area video
            for area in data.find_all(
                "ytd-video-renderer", class_="style-scope ytd-item-section-renderer"
            ):
                video = {}

                # Mengambil title
                title_tag = area.find("a", id="video-title")
                if title_tag:
                    video["Title"] = title_tag["title"]
                    video["Link"] = f"https://www.youtube.com{title_tag['href']}"

                # Mengambil views
                views_tag = area.find("span", class_="style-scope ytd-video-meta-block")
                if views_tag:
                    video["Views"] = views_tag.text.strip()

                # Mengambil channel
                channel_tag = area.find(
                    "a", class_="yt-simple-endpoint style-scope yt-formatted-string"
                )
                if channel_tag:
                    video["Channel"] = channel_tag.text.strip()

                video_data.append(video)

            driver.quit()
            return video_data
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            driver.quit()
            time.sleep(random.uniform(1, 3))
        finally:
            if driver:
                driver.quit()
    return []


# Mengambil data dari halaman secara paralel
all_video_data = get_page_data()

# Membuat DataFrame dari list video_data
df = pd.DataFrame(all_video_data)

# Mengekspor DataFrame ke file Excel
df.to_excel("youtube_data_all_pages.xlsx", index=False)

print("Data berhasil diekspor ke youtube_data_all_pages.xlsx")
