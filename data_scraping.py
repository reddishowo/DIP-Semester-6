import requests
from bs4 import BeautifulSoup
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_english(text):
    english_pattern = re.compile(r'^[a-zA-Z0-9\s\.,!?\'\"()-_:;]+$')
    words = text.split()
    if not words:
        return False
   
    english_words = 0
    for word in words:
        if english_pattern.match(word):
            english_words += 1
   
    return (english_words / len(words)) >= 0.7

# App ID untuk Apex Legends
app_id = "1172470"
base_url = f"https://steamcommunity.com/app/{app_id}/reviews/?browsefilter=toprated&snr=1_5_100010_"
all_reviews = []
max_scroll_attempts = 100  # Jumlah maksimum percobaan scroll
min_new_reviews = 3  # Berhenti jika kurang dari ini ditemukan dalam percobaan scroll

# Set up Selenium dengan Firefox
firefox_options = Options()
# Hilangkan komentar pada headless mode jika tidak ingin melihat browser
# firefox_options.add_argument("--headless")
firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0")

driver = webdriver.Firefox(options=firefox_options)

try:
    # Buka halaman reviews
    url = base_url
    print(f"Mengakses URL: {url}")
    driver.get(url)
    
    # Tunggu review pertama dimuat
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "apphub_CardTextContent"))
    )
    
    # Variabel untuk melacak jumlah review yang dikumpulkan pada scroll sebelumnya
    previous_review_count = 0
    consecutive_no_new_reviews = 0
    
    # Scroll ke bawah untuk memuat lebih banyak review
    for scroll_attempt in range(max_scroll_attempts):
        # Scroll ke bawah
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolling attempt #{scroll_attempt+1}")
        
        # Tunggu konten baru dimuat (biasanya ada animasi loading)
        time.sleep(3)
        
        # Ambil sumber halaman setelah eksekusi JavaScript
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Temukan semua blok review
        review_blocks = soup.find_all('div', class_='apphub_Card')
        
        # Ekstrak review dari halaman
        page_reviews = []
        for block in review_blocks:
            try:
                # Temukan teks review
                review_text_element = block.find('div', class_='apphub_CardTextContent')
                if review_text_element:
                    # Hapus baris tanggal dan elemen non-review lainnya
                    for date_line in review_text_element.find_all('div', class_='date_posted'):
                        date_line.decompose()
                    
                    # Bersihkan teks
                    review_text = review_text_element.get_text(strip=True)
                    
                    # Hapus awalan "Posted: " yang terkadang muncul
                    review_text = re.sub(r'^Posted:\s*', '', review_text)
                    
                    # Pembersihan tambahan jika diperlukan
                    review_text = re.sub(r'\s+', ' ', review_text)  # Ganti beberapa spasi dengan satu spasi
                    
                    if review_text and is_english(review_text):
                        # Periksa apakah review ini duplikat
                        if review_text not in page_reviews:
                            page_reviews.append(review_text)
            except Exception as e:
                print(f"Error memproses review: {e}")
        
        # Periksa duplikat terhadap koleksi yang sudah ada
        new_reviews = [r for r in page_reviews if r not in all_reviews]
        all_reviews.extend(new_reviews)
        
        print(f"Total review yang dikumpulkan: {len(all_reviews)} (Baru: {len(new_reviews)})")
        
        # Periksa apakah kita mendapatkan review baru yang cukup
        if len(new_reviews) < min_new_reviews:
            consecutive_no_new_reviews += 1
            print(f"Hanya menemukan {len(new_reviews)} review baru. ({consecutive_no_new_reviews}/3 percobaan)")
            
            # Jika 3 kali berturut-turut mendapatkan sedikit review baru, hentikan
            if consecutive_no_new_reviews >= 3:
                print("Tidak ada review baru yang cukup setelah 3 percobaan berturut-turut. Berhenti scrolling.")
                break
        else:
            # Reset counter jika kita mendapatkan review baru yang cukup
            consecutive_no_new_reviews = 0
        
        # Tunda acak antara permintaan untuk menghindari pemblokiran
        sleep_time = random.uniform(2, 5)
        print(f"Menunggu {sleep_time:.2f} detik sebelum scroll berikutnya...")
        time.sleep(sleep_time)

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    
    # Simpan semua review bahasa Inggris yang dikumpulkan
    with open("apex_legends_english_reviews.txt", "w", encoding="utf-8") as file:
        for review in all_reviews:
            file.write(f"{review}\n\n")

    print(f"Berhasil menyimpan {len(all_reviews)} review bahasa Inggris yang unik")