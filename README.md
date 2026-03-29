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

### Persiapan

**Sumber data:** [Students' Performance Dataset - Dicoding](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

**Setup environment:**

```bash
pip install -r requirements.txt
```

---

## Business Dashboard

Dashboard dibuat menggunakan **Google Looker Studio** untuk memantau performa siswa secara visual dan interaktif. Dashboard menampilkan:

- Distribusi status siswa (Graduate 49.9%, Dropout 32.1%, Enrolled 17.9%)
- Persentase pembayaran SPP tepat waktu per status
- Distribusi usia saat pendaftaran per status
- Rata-rata nilai semester 1 & 2 per status
- Persentase penerima beasiswa per status
- Rata-rata unit yang lulus per semester per status

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

🔗 **Link Prototype:** [https://jaya-jaya-dropout-silvio.streamlit.app](https://jaya-jaya-dropout-silvio.streamlit.app)

### Cara Menggunakan Aplikasi

1. Buka aplikasi di browser
2. Isi data siswa: informasi pribadi, akademik, dan keuangan
3. Masukkan performa semester 1 dan semester 2
4. Klik tombol **"Prediksi Risiko Dropout"**
5. Sistem akan menampilkan prediksi (Berisiko/Tidak Berisiko) beserta probabilitasnya
6. Jika berisiko, sistem akan memberikan rekomendasi tindakan yang perlu dilakukan

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

5. **Usia saat mendaftar**: Siswa dropout rata-rata lebih tua (26.1 tahun) dibanding Graduate (21.8 tahun), mengindikasikan tanggung jawab di luar studi yang lebih besar

6. Model **Random Forest** mencapai **accuracy 88.02%** dengan **AUC-ROC 0.9293** untuk prediksi dropout — menunjukkan model mampu memisahkan siswa berisiko dengan cukup baik

### Rekomendasi Action Items

- **Sistem Deteksi Dini Berbasis Model**: Terapkan sistem prediksi ini di akhir semester 1, fokus pada siswa dengan nilai rendah dan sedikit unit lulus. Siswa yang terdeteksi berisiko segera diberikan pendampingan akademik intensif

- **Program Bantuan Keuangan Proaktif**: Perluas beasiswa dan keringanan SPP bagi siswa yang mengalami kesulitan finansial. Monitoring status pembayaran SPP secara rutin dan hubungi siswa yang terlambat bayar sebelum situasinya memburuk

- **Intervensi Akademik Semester 1**: Lakukan evaluasi akademik di pertengahan semester 1 (bukan hanya akhir semester) sehingga siswa yang mulai tertinggal bisa mendapat bantuan lebih awal — karena nilai semester 1 sudah sangat prediktif terhadap dropout

- **Program Dukungan untuk Mahasiswa Dewasa**: Buat program khusus untuk mahasiswa yang mendaftar di usia lebih tua (25+ tahun), seperti jadwal kelas yang fleksibel atau program part-time, mengingat kelompok ini memiliki risiko dropout lebih tinggi

- **Perluasan Program Beasiswa**: Tingkatkan jumlah dan akses beasiswa mengingat perbedaan yang sangat besar antara penerima beasiswa di kelompok Graduate (37.8%) vs Dropout (9.4%). Beasiswa terbukti jadi faktor protektif yang kuat
