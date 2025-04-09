# Analisis dan Pemrosesan Dataset Credit Card Fraud Detection

## Deskripsi Proyek
Proyek ini merupakan tugas dari mata kuliah *Data, Informasi, dan Pengetahuan* yang bertujuan untuk menganalisis dataset dengan distribusi kelas tidak seimbang (*imbalanced*), melakukan pra-pemrosesan, menerapkan teknik balancing, dan membagi data menjadi *training* dan *testing set*. Dataset yang digunakan adalah "Credit Card Fraud Detection" dari Kaggle, yang berisi data transaksi kartu kredit dengan kelas mayoritas (transaksi normal) dan kelas minoritas (transaksi fraud). Proyek ini menggunakan teknik SMOTE untuk menyeimbangkan kelas dan menyertakan visualisasi distribusi kelas sebelum serta sesudah pemrosesan.

### Tujuan
1. Melakukan eksplorasi awal dataset dan visualisasi distribusi kelas.
2. Menerapkan normalisasi pada fitur numerik menggunakan MinMaxScaler.
3. Menyeimbangkan kelas menggunakan SMOTE (*Synthetic Minority Oversampling Technique*).
4. Membagi dataset menjadi *training set* (80%) dan *testing set* (20%) dengan proporsi kelas yang terjaga.
5. Menyusun laporan singkat dalam format PDF.

## Dataset
- **Nama**: Credit Card Fraud Detection
- **Sumber**: [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
- **Deskripsi**: Dataset berisi 284,807 transaksi kartu kredit dengan 31 kolom, termasuk `Time`, `Amount`, 28 fitur anonim (V1-V28), dan kolom target `Class` (0 untuk normal, 1 untuk fraud).
- **Distribusi Awal**:
  - Kelas 0 (Normal): 284,315 instance (99.83%)
  - Kelas 1 (Fraud): 492 instance (0.17%)

## Prasyarat
Untuk menjalankan proyek ini, Anda perlu menginstal dependensi berikut:
- Python 3.8 atau lebih tinggi
- Library Python:
  ```
  pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn
  ```

## Struktur File
```
├── creditcard.csv          # Dataset Credit Card Fraud Detection
├── analysis.ipynb          # Notebook dengan kode analisis dan visualisasi
└── README.md               
```


## Hasil Utama
- **Distribusi Sebelum Balancing**: Kelas 0: 284,315, Kelas 1: 492.
- **Distribusi Setelah SMOTE**: Kelas 0: 284,315, Kelas 1: 284,315.
- **Splitting Data**:
  - *Training Set*: Kelas 0: 227,452, Kelas 1: 227,452.
  - *Testing Set*: Kelas 0: 56,863, Kelas 1: 56,863.
- Visualisasi distribusi kelas sebelum dan sesudah balancing, serta setelah splitting, tersedia di notebook.


