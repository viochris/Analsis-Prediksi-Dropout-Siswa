# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan Jaya Jaya Institut

- **Nama**: Silvio Christian Joe
- **Email**: viochristian12@gmail.com
- **ID Dicoding**: silvio

---

## Business Understanding

Jaya Jaya Institut adalah institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan mencetak banyak lulusan dengan reputasi baik. Namun, tantangan besar yang dihadapi adalah tingginya angka **dropout siswa** yang berpotensi merusak reputasi dan keberlangsungan institusi.

### Permasalahan Bisnis

- Tingginya angka dropout siswa (32.1% dari total 4.424 siswa, atau **1.421 siswa**)
- Institusi belum memiliki sistem deteksi dini untuk mengidentifikasi siswa yang berisiko dropout
- Kurangnya pemahaman tentang faktor-faktor utama yang mendorong siswa untuk keluar sebelum menyelesaikan pendidikan
- Tidak ada mekanisme monitoring performa siswa secara sistematis dan berbasis data

### Cakupan Proyek

- Eksplorasi dan analisis data performa siswa (4.424 siswa, 36 fitur)
- Identifikasi faktor-faktor utama yang berkontribusi pada dropout
- Pembuatan business dashboard untuk monitoring performa siswa
- Pengembangan model machine learning untuk memprediksi risiko dropout
- Deployment prototype aplikasi prediksi berbasis Streamlit

### Link Github
> 🔗 **Link Github:** [https://github.com/viochris/Analsis-Prediksi-Dropout-Siswa](https://github.com/viochris/Analsis-Prediksi-Dropout-Siswa)

### Persiapan

**Sumber data:** [Students' Performance Dataset - Dicoding](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

**Setup Environment:**
Proyek ini dikembangkan dan diuji menggunakan **Python 3.12**. Sangat disarankan untuk menggunakan versi Python yang sama atau kompatibel untuk menghindari konflik *dependency*.

Berikut adalah langkah-langkah untuk menyiapkan *environment* dan menjalankan proyek ini secara lokal:

1. **Clone/Download Repository**
   Pastikan Anda sudah berada di dalam direktori proyek ini.
   > 🔗 **Link Github:** [https://github.com/viochris/Analsis-Prediksi-Dropout-Siswa](https://github.com/viochris/Analsis-Prediksi-Dropout-Siswa)

2. **Buat Virtual Environment**
   Langkah ini penting untuk menjaga agar *library* proyek terisolasi. Jalankan perintah berikut di terminal:
   ```bash
   # Untuk pengguna Windows
   python -m venv venv
   
   # Untuk pengguna Mac/Linux
   python3 -m venv venv
   ```

3. **Aktifkan Virtual Environment**
   ```bash
   # Untuk pengguna Windows (Command Prompt)
   venv\Scripts\activate
   # Untuk pengguna Windows (Git Bash/PowerShell)
   source venv/Scripts/activate
   
   # Untuk pengguna Mac/Linux
   source venv/bin/activate
   ```

4. **Install Dependencies**
   Setelah virtual environment aktif (terlihat tulisan `(venv)` di terminal), install semua *library* yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## Business Dashboard

Dashboard dibuat menggunakan **Google Looker Studio** untuk memantau performa siswa secara visual dan interaktif.

**Catatan penting:** Dataset yang digunakan untuk dashboard hanya mencakup siswa dengan status **Dropout** dan **Graduate** (tanpa Enrolled). Hal ini karena siswa Enrolled masih aktif berkuliah dan belum memiliki outcome akhir yang jelas, sehingga memasukkan mereka berpotensi menimbulkan bias dalam analisis dan menyesatkan interpretasi.

Dashboard menampilkan:

- Distribusi status siswa (Graduate vs Dropout)
- Persentase pembayaran SPP tepat waktu per status
- Distribusi usia saat pendaftaran per status (dengan legend warna yang jelas)
- Rata-rata nilai semester 1 & 2 per status
- Persentase penerima beasiswa per status
- Rata-rata jumlah mata kuliah yang lulus per semester per status

🔗 **Link Dashboard:** [https://lookerstudio.google.com/reporting/33f6debd-60a5-4541-881d-bfb4f279cfbb](https://lookerstudio.google.com/reporting/33f6debd-60a5-4541-881d-bfb4f279cfbb)

*(Screenshot dashboard tersedia di file `silvio-dashboard.png`)*

---

## Menjalankan Sistem Machine Learning

### Jalankan Lokal

```bash
# Pastikan berada di folder submission
pip install -r requirements.txt

# Jalankan aplikasi Streamlit
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

### Akses Online (Streamlit Community Cloud)

🔗 **Link Prototype:** [https://jaya-jaya-dropout-silvio.streamlit.app](https://jaya-jaya-dropout-silvio.streamlit.app/)

### Cara Menggunakan Aplikasi

1. Buka aplikasi di browser
2. Isi **semua** data siswa: informasi pribadi, akademik, keuangan, data orang tua, performa semester 1 dan 2, serta kondisi ekonomi makro (total 36 fitur)
3. Klik tombol **"Prediksi Risiko Dropout"**
4. Sistem akan menampilkan prediksi (Berisiko/Tidak Berisiko) beserta probabilitasnya
5. Jika berisiko, sistem akan memberikan rekomendasi tindakan yang perlu dilakukan

---

## Penjelasan Proses Pengolahan Data

### Data Understanding

Dataset berisi **4.424 data siswa** dengan **36 fitur** dan 1 kolom target (`Status`) yang memiliki 3 nilai: Graduate, Dropout, dan Enrolled.

Sebelum membangun model, penting untuk memahami semua kelas yang ada:

| Status    | Jumlah | Persentase |
|-----------|--------|------------|
| Graduate  | 2.209  | 49.9%      |
| Dropout   | 1.421  | 32.1%      |
| Enrolled  | 794    | 17.9%      |

### Data Preparation

Tujuan model adalah memprediksi apakah siswa akan **Dropout atau Graduate**. Oleh karena itu, pada tahap preparation dilakukan **filtering data** untuk hanya menyertakan siswa dengan status Dropout dan Graduate.

**Alasan filtering Enrolled:**

Siswa dengan status Enrolled masih aktif berkuliah dan belum memiliki outcome yang jelas (belum lulus atau dropout). Jika Enrolled ikut ditraining dengan encoding yang sama dengan Graduate (keduanya dijadikan kelas 0), maka target menjadi **ambigu** karena dua kelompok dengan karakteristik berbeda digabungkan dalam satu label. Ini akan menurunkan validitas dan performa model.

**Hasil filtering:**

- Sebelum: 4.424 baris
- Setelah (hanya Dropout & Graduate): 3.630 baris
- Target encoding: Dropout = 1, Graduate = 0

**Scaling data:**

Proses scaling menggunakan `StandardScaler` dilakukan pada tahap Data Preparation (sebelum modeling), bukan di dalam tahap Modeling. Ini sesuai dengan praktik yang baik karena scaling merupakan bagian dari preprocessing data.

### Fitur yang Digunakan

Semua **36 fitur** digunakan dalam pemodelan, mencakup:
- Informasi demografis (usia, jenis kelamin, status pernikahan, nasionalitas)
- Informasi akademik (mode aplikasi, program studi, nilai masuk, kualifikasi sebelumnya)
- Informasi keuangan (pembayaran SPP, status debtor, beasiswa)
- Informasi keluarga (kualifikasi dan pekerjaan orang tua)
- Performa akademik semester 1 dan 2 (unit terdaftar, lulus, nilai, evaluasi)
- Kondisi ekonomi makro (pengangguran, inflasi, GDP)

Jumlah fitur di Streamlit **sama persis** dengan jumlah fitur yang digunakan saat training (36 fitur).

### Alur Notebook

| Tahap | Isi |
|-------|-----|
| **Data Understanding** | EDA, distribusi, korelasi, visualisasi |
| **Data Preparation** | Filter Dropout & Graduate, encoding target, split train/test, **scaling (StandardScaler)**, export CSV dashboard |
| **Modeling** | Pemilihan algoritma, penentuan hyperparameter, training model |
| **Evaluation** | Accuracy, AUC-ROC, confusion matrix, feature importance |

---

## Conclusion

Berdasarkan analisis data dan model machine learning yang dikembangkan, ditemukan beberapa kesimpulan penting:

1. **Dropout rate** Jaya Jaya Institut mencapai **32.1%** (1.421 dari 4.424 siswa) — hampir 1 dari 3 siswa tidak menyelesaikan studinya

2. **Performa akademik** adalah prediktor terkuat dropout:
   - Siswa dropout yang memiliki nilai rata-rata semester 1 hanya **7.26** (Graduate: 12.64)
   - Rata-rata unit yang lulus semester 2 dan merupakan siswa dropout hanya **1.9 unit** (Graduate: 6.2 unit)

3. **Masalah keuangan** sangat berkorelasi dengan dropout:
   - Hanya **67.8%** siswa dropout membayar SPP tepat waktu (Graduate: 98.7%)
   - **22%** siswa dropout berstatus debtor, dibanding Graduate yang hanya 4.6%

4. **Beasiswa sebagai faktor protektif**: Hanya **9.4%** siswa dropout yang menerima beasiswa, dibandingkan **37.8%** pada kelompok Graduate

5. **Usia saat mendaftar**: Siswa dropout rata-rata lebih tua (26.1 tahun) dibanding Graduate (21.8 tahun)

6. Model **Random Forest** dilatih pada data Dropout dan Graduate (3.630 siswa) dengan seluruh **36 fitur**, menghasilkan performa yang valid karena target encoding tidak ambigu (hanya dua kelas yang jelas). Dengan akurasi 0.9284 dan AUC-ROC score 0.9711

### Rekomendasi Action Items

- **Sistem Deteksi Dini Berbasis Model**: Terapkan sistem prediksi ini di akhir semester 1, fokus pada siswa dengan nilai rendah dan sedikit unit lulus. Siswa yang terdeteksi berisiko segera diberikan pendampingan akademik intensif

- **Program Bantuan Keuangan Proaktif**: Perluas beasiswa dan keringanan SPP bagi siswa yang mengalami kesulitan finansial. Monitoring status pembayaran SPP secara rutin dan hubungi siswa yang terlambat bayar sebelum situasinya memburuk

- **Intervensi Akademik Semester 1**: Lakukan evaluasi akademik di pertengahan semester 1 sehingga siswa yang mulai tertinggal bisa mendapat bantuan lebih awal

- **Program Dukungan untuk Mahasiswa Dewasa**: Buat program khusus untuk mahasiswa yang mendaftar di usia lebih tua (25+ tahun), seperti jadwal kelas yang fleksibel atau program part-time

- **Perluasan Program Beasiswa**: Tingkatkan jumlah dan akses beasiswa mengingat perbedaan yang sangat besar antara penerima beasiswa di kelompok Graduate (37.8%) vs Dropout (9.4%)
