# Eksplorasi dan Pembersihan Data: NYC Airbnb Open Data

## Deskripsi Proyek
Proyek ini merupakan tugas dari mata kuliah **Data, Informasi, dan Pengetahuan** yang bertujuan untuk melatih kemampuan eksplorasi dan pembersihan data menggunakan Python dan library Pandas. Dataset yang digunakan adalah **"New York City Airbnb Open Data"** dari Kaggle, yang berisi lebih dari 48.000 baris data tentang daftar penyewaan Airbnb di New York City. Proyek ini mencakup identifikasi dan penanganan masalah seperti *missing values*, *outliers*, *noise*, *data duplicates*, serta inkonsistensi data, diikuti dengan simulasi integrasi dua dataset sederhana.

## Dataset
- **Nama**: New York City Airbnb Open Data
- **Sumber**: [Kaggle](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data)
- **Ukuran**: >48.000 baris, 16 kolom
- **Kolom Utama**:
  - `id`: ID listing
  - `name`: Nama listing
  - `host_name`: Nama host
  - `price`: Harga per malam (USD)
  - `last_review`: Tanggal ulasan terakhir
  - `reviews_per_month`: Jumlah ulasan per bulan

## Struktur Direktori
```
/NYC-Airbnb-Data-Cleaning
├── AB_NYC_2019.csv          # Dataset asli dari Kaggle
├── cleaned_nyc_airbnb.csv   # Dataset hasil cleaning
├── data_cleaning.ipynb      # Jupyter Notebook dengan kode cleaning
└── README.md                
```

## Langkah-langkah Pembersihan
1. **Eksplorasi Awal**:
   - Memuat dataset dan menampilkan informasi struktur (`df.info()`, `df.describe()`).
2. **Missing Values**:
   - Mengisi `name` dan `host_name` dengan "Unknown".
   - Mengisi `last_review` dengan "No Review" dan `reviews_per_month` dengan 0.
3. **Outliers**:
   - Menghapus nilai ekstrem pada `price` menggunakan metode IQR.
4. **Noise**:
   - Menghapus 11 entri dengan harga <= 0 (contoh: ID 18750597).
5. **Data Duplicates**:
   - Memeriksa dan menghapus duplikat jika ada.
6. **Integrasi dan Koreksi**:
   - Menggabungkan dataset utama dengan dataset transaksi simulasi (5 baris).
   - Menstandarisasi format tanggal pada `last_review`.

## Prasyarat
Untuk menjalankan proyek ini, Anda perlu menginstal dependensi berikut:
- Python 3.8+
- Pandas
- NumPy
- Matplotlib

Instal dependensi dengan:
```bash
pip install pandas numpy matplotlib
```

## Temuan Utama
- **Missing Values**: Terdapat nilai kosong pada `name`, `host_name`, `last_review`, dan `reviews_per_month`.
- **Outliers**: Harga ekstrem pada `price` dihapus untuk normalisasi data.
- **Noise**: 11 listing dengan harga <= 0 diidentifikasi dan dihapus.
- **Integrasi**: Dataset utama berhasil digabungkan dengan data transaksi simulasi.

