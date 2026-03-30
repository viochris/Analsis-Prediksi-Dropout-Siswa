import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Config ---
st.set_page_config(
    page_title="Prediksi Dropout Siswa - Jaya Jaya Institut",
    page_icon="🎓",
    layout="centered"
)

# --- Load Model ---
@st.cache_resource
def load_model():
    model = joblib.load('model/model.pkl')
    feature_names = joblib.load('model/feature_names.pkl')
    return model, feature_names

model, feature_names = load_model()

# --- UI ---
st.title("🎓 Prediksi Risiko Dropout Siswa")
st.markdown("**Jaya Jaya Institut** — Sistem prediksi untuk mendeteksi siswa yang berisiko dropout lebih awal.")
st.divider()

st.subheader("Isi Data Siswa")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Informasi Pribadi**")
    marital_status = st.selectbox("Status Pernikahan",
                                   options=[1, 2, 3, 4, 5, 6],
                                   format_func=lambda x: {1:'Lajang (Single)', 2:'Menikah (Married)', 3:'Duda/Janda (Widower)',
                                                          4:'Cerai (Divorced)', 5:'Kumpul Kebo (Facto Union)', 6:'Pisah Legal (Legally Separated)'}[x])
    gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: 'Laki-laki' if x==1 else 'Perempuan')
    age_at_enrollment = st.number_input("Usia saat Mendaftar (tahun)", min_value=17, max_value=70, value=20)

    nacionality_dict = {
        1: 'Portugal', 2: 'Jerman', 6: 'Spanyol', 11: 'Italia', 13: 'Belanda',
        14: 'Inggris', 17: 'Lithuania', 21: 'Angola', 22: 'Tanjung Verde',
        24: 'Guinea', 25: 'Mozambik', 26: 'Sao Tome', 32: 'Turki',
        41: 'Brasil', 62: 'Rumania', 100: 'Moldova',
        101: 'Meksiko', 103: 'Ukraina', 105: 'Rusia', 108: 'Kuba', 109: 'Kolombia'
    }
    nacionality = st.selectbox("Kewarganegaraan",
                               options=list(nacionality_dict.keys()),
                               format_func=lambda x: nacionality_dict[x])

    displaced = st.selectbox("Perantau (tinggal jauh dari kota asal)?", options=[0, 1],
                              format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    international = st.selectbox("Mahasiswa Internasional (dari luar negeri)?", options=[0, 1],
                                  format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    educational_special_needs = st.selectbox("Memiliki Kebutuhan Pendidikan Khusus?", options=[0, 1],
                                              format_func=lambda x: 'Ya' if x==1 else 'Tidak')

with col2:
    st.markdown("**Informasi Akademik & Keuangan**")
    course = st.selectbox("Program Studi",
                           options=[33, 171, 8014, 9003, 9070, 9085, 9119, 9130,
                                    9147, 9238, 9254, 9500, 9556, 9670, 9773, 9853, 9991],
                           format_func=lambda x: {
                               33:'Teknologi Produksi Biofuel', 171:'Animasi & Desain Multimedia',
                               8014:'Layanan Sosial (Malam)', 9003:'Agronomi', 9070:'Desain Komunikasi',
                               9085:'Keperawatan Hewan', 9119:'Teknik Informatika', 9130:'Ekuikultur',
                               9147:'Manajemen', 9238:'Layanan Sosial', 9254:'Pariwisata', 9500:'Keperawatan',
                               9556:'Kebersihan Mulut', 9670:'Manajemen Periklanan & Pemasaran',
                               9773:'Jurnalisme & Komunikasi', 9853:'Pendidikan Dasar',
                               9991:'Manajemen (Malam)'
                           }[x])
    daytime_evening = st.selectbox("Waktu Kuliah", options=[1, 0],
                                    format_func=lambda x: 'Pagi/Siang' if x==1 else 'Malam')

    app_mode_dict = {
        1: '1st phase - general contingent', 2: 'Ordinance No. 612/93',
        5: '1st phase - special contingent (Azores Island)',
        7: 'Holders of other higher courses', 10: 'Ordinance No. 854-B/99',
        15: 'International student (bachelor)',
        16: '1st phase - special contingent (Madeira Island)',
        17: '2nd phase - general contingent', 18: '3rd phase - general contingent',
        26: 'Ordinance No. 533-A/99, item b2)',
        27: 'Ordinance No. 533-A/99, item b3 (Other Institution)',
        39: 'Over 23 years old', 42: 'Transfer', 43: 'Change of course',
        44: 'Technological specialization diploma holders',
        51: 'Change of institution/course',
        53: 'Short cycle diploma holders',
        57: 'Change of institution/course (International)'
    }
    application_mode = st.selectbox("Jalur Pendaftaran Masuk",
                                    options=list(app_mode_dict.keys()),
                                    format_func=lambda x: app_mode_dict[x],
                                    index=7)

    application_order = st.selectbox("Urutan Pilihan Program Studi",
                                     options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                     format_func=lambda x: f"Pilihan ke-{x}" if x > 0 else "Pilihan Pertama (0)")

    prev_qual_dict = {
        1: 'SMA/Sederajat (Secondary Education)',
        2: "S1 - Sarjana (Bachelor's Degree)",
        3: 'S1 - Gelar Akademik (Degree)',
        4: "S2 - Magister (Master's)",
        5: 'S3 - Doktor (Doctorate)',
        6: 'Sedang Menempuh Pendidikan Tinggi',
        9: 'Kelas 12 - Tidak Lulus',
        10: 'Kelas 11 - Tidak Lulus',
        12: 'Lainnya - Kelas 11',
        14: 'Kelas 10',
        15: 'Kelas 10 - Tidak Lulus',
        19: 'Pendidikan Dasar Siklus 3 (Setara SMP/SMA)',
        38: 'Pendidikan Dasar Siklus 2 (Setara SD-SMP)',
        39: 'Kursus Spesialisasi Teknologi',
        40: 'Pendidikan Tinggi - Sarjana (Siklus 1)',
        42: 'Kursus Teknik Tinggi Profesional',
        43: 'Pendidikan Tinggi - Magister (Siklus 2)'
    }
    previous_qualification = st.selectbox("Pendidikan Terakhir Sebelum Masuk",
                                          options=list(prev_qual_dict.keys()),
                                          format_func=lambda x: prev_qual_dict[x])

    prev_qual_grade = st.slider("Nilai Ijazah/Kualifikasi Sebelumnya (0–200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    admission_grade = st.slider("Nilai Masuk / Seleksi Penerimaan (0–200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    tuition_fees = st.selectbox("Uang Kuliah (SPP) Dibayar Tepat Waktu?", options=[1, 0],
                                 format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    debtor = st.selectbox("Memiliki Tunggakan/Hutang ke Kampus?", options=[0, 1],
                          format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    scholarship = st.selectbox("Penerima Beasiswa?", options=[0, 1],
                                format_func=lambda x: 'Ya' if x==1 else 'Tidak')

st.markdown("**Latar Belakang Pendidikan & Pekerjaan Orang Tua**")

qual_dict = {
    1: 'SMA/Sederajat', 2: "S1 Sarjana", 3: 'Gelar Akademik',
    4: "S2 Magister", 5: 'S3 Doktor', 6: 'Sedang Kuliah',
    9: 'Kelas 12 Tidak Lulus', 10: 'Kelas 11 Tidak Lulus',
    11: 'Tahun ke-7 (Lama)', 12: 'Lainnya - Kelas 11', 13: 'Tambahan 2 Tahun',
    14: 'Kelas 10', 15: 'Kelas 10 Tidak Lulus',
    18: 'Kursus Perdagangan Umum', 19: 'Pendidikan Dasar Siklus 3 (Setara SMP)',
    20: 'Kursus SMA Komplementer', 22: 'Kursus Teknik-Profesional',
    25: 'Kursus Sekretaris & Perdagangan', 26: 'Kelas 11', 27: 'Siklus 2 SMA Umum',
    29: 'Kelas 9 Tidak Lulus', 30: 'Kelas 8', 31: 'Kursus Admin & Perdagangan',
    33: 'Akuntansi & Admin Lanjutan', 34: 'Tidak Diketahui',
    35: 'Tidak Bisa Baca/Tulis', 36: 'Bisa Baca Tanpa Ijazah Kelas 4',
    37: 'Pendidikan Dasar Siklus 1 (Setara SD)',
    38: 'Pendidikan Dasar Siklus 2 (Setara SD-SMP)',
    39: 'Kursus Spesialisasi Teknologi', 40: 'Sarjana (Siklus 1)',
    41: 'Studi Tinggi Khusus', 42: 'Kursus Teknik Tinggi Profesional',
    43: 'Magister (Siklus 2)', 44: 'Doktor (Siklus 3)'
}

occ_dict = {
    0: 'Mahasiswa/Pelajar', 1: 'Pejabat Legislatif/Eksekutif',
    2: 'Tenaga Ahli Intelektual/Ilmiah', 3: 'Teknisi Tingkat Menengah',
    4: 'Staf Administrasi', 5: 'Pekerja Jasa, Keamanan & Penjualan',
    6: 'Petani & Pekerja Pertanian', 7: 'Pekerja Terampil Industri & Konstruksi',
    8: 'Operator Mesin & Perakitan', 9: 'Pekerja Tidak Terampil',
    10: 'Profesi Militer', 90: 'Situasi Lain', 99: '(Kosong/Tidak Ada Data)',
    101: 'Perwira Militer', 102: 'Sersan Militer', 103: 'Personel Militer Lainnya',
    112: 'Direktur Layanan Administratif', 114: 'Direktur Hotel/Restoran',
    121: 'Ahli Fisika, Matematika, Teknik', 122: 'Tenaga Kesehatan Profesional',
    123: 'Guru/Pengajar', 124: 'Ahli Keuangan, Akuntansi, Admin',
    125: 'Spesialis TIK', 131: 'Teknisi Sains/Teknik', 132: 'Teknisi Kesehatan',
    134: 'Teknisi Hukum/Sosial/Budaya', 135: 'Teknisi TIK',
    141: 'Staf Kantor/Sekretaris', 143: 'Operator Data/Akuntansi',
    144: 'Staf Administrasi Lainnya', 151: 'Pekerja Layanan Pribadi',
    152: 'Tenaga Penjual', 153: 'Pekerja Perawatan Pribadi',
    154: 'Petugas Keamanan/Perlindungan', 161: 'Petani Berorientasi Pasar',
    163: 'Peternak', 171: 'Pekerja Konstruksi Terampil',
    172: 'Pekerja Metalurgi Terampil', 174: 'Pekerja Listrik/Elektronik Terampil',
    175: 'Pekerja Industri Makanan, Kayu, Pakaian',
    181: 'Operator Pabrik/Mesin Stasioner', 182: 'Pekerja Perakitan',
    183: 'Pengemudi/Operator Kendaraan', 192: 'Pekerja Tidak Terampil Pertanian/Perikanan',
    193: 'Pekerja Tidak Terampil Industri/Konstruksi',
    194: 'Asisten Persiapan Makanan', 195: 'Pedagang Kaki Lima'
}

col3, col4 = st.columns(2)
with col3:
    m_qual_opts = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 14, 18, 19, 22, 26, 27, 29, 30, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
    m_occ_opts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 90, 99, 122, 123, 125, 131, 132, 134, 141, 143, 144, 151, 152, 153, 171, 173, 175, 191, 192, 193, 194]

    mothers_qualification = st.selectbox("Pendidikan Terakhir Ibu",
                                         options=m_qual_opts, index=12,
                                         format_func=lambda x: qual_dict.get(x, f'Kode {x}'))
    mothers_occupation = st.selectbox("Pekerjaan Ibu",
                                      options=m_occ_opts, index=5,
                                      format_func=lambda x: occ_dict.get(x, f'Kode {x}'))

with col4:
    f_qual_opts = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 18, 19, 20, 22, 25, 26, 27, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
    f_occ_opts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 90, 99, 101, 102, 103, 112, 114, 121, 122, 123, 124, 131, 132, 134, 135, 141, 143, 144, 151, 152, 153, 154, 161, 163, 171, 172, 174, 175, 181, 182, 183, 192, 193, 194, 195]

    fathers_qualification = st.selectbox("Pendidikan Terakhir Ayah",
                                         options=f_qual_opts, index=13,
                                         format_func=lambda x: qual_dict.get(x, f'Kode {x}'))
    fathers_occupation = st.selectbox("Pekerjaan Ayah",
                                      options=f_occ_opts, index=5,
                                      format_func=lambda x: occ_dict.get(x, f'Kode {x}'))

st.divider()
st.subheader("Performa Akademik Semester 1")
col5, col6 = st.columns(2)

with col5:
    cu1_credited = st.number_input("Mata Kuliah yang Di-kredit (Sem. 1)", min_value=0, max_value=20, value=0,
                                    help="Jumlah mata kuliah yang diakui dari institusi/program sebelumnya")
    cu1_enrolled = st.number_input("Mata Kuliah yang Diambil (Sem. 1)", min_value=0, max_value=30, value=6,
                                    help="Jumlah mata kuliah yang didaftarkan di semester 1")
    cu1_evaluations = st.number_input("Jumlah Ujian/Evaluasi (Sem. 1)", min_value=0, max_value=40, value=6,
                                       help="Jumlah evaluasi/ujian yang diikuti di semester 1")

with col6:
    cu1_approved = st.number_input("Mata Kuliah yang Lulus (Sem. 1)", min_value=0, max_value=30, value=5,
                                    help="Jumlah mata kuliah yang berhasil lulus di semester 1")
    cu1_grade = st.slider("Nilai Rata-rata Semester 1 (0–20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu1_no_eval = st.number_input("Mata Kuliah Tanpa Evaluasi (Sem. 1)", min_value=0, max_value=20, value=0,
                                   help="Jumlah mata kuliah yang tidak mengikuti evaluasi")

st.subheader("Performa Akademik Semester 2")
col7, col8 = st.columns(2)

with col7:
    cu2_credited = st.number_input("Mata Kuliah yang Di-kredit (Sem. 2)", min_value=0, max_value=20, value=0,
                                    help="Jumlah mata kuliah yang diakui dari institusi/program sebelumnya")
    cu2_enrolled = st.number_input("Mata Kuliah yang Diambil (Sem. 2)", min_value=0, max_value=30, value=6,
                                    help="Jumlah mata kuliah yang didaftarkan di semester 2")
    cu2_evaluations = st.number_input("Jumlah Ujian/Evaluasi (Sem. 2)", min_value=0, max_value=40, value=6,
                                       help="Jumlah evaluasi/ujian yang diikuti di semester 2")

with col8:
    cu2_approved = st.number_input("Mata Kuliah yang Lulus (Sem. 2)", min_value=0, max_value=30, value=5,
                                    help="Jumlah mata kuliah yang berhasil lulus di semester 2")
    cu2_grade = st.slider("Nilai Rata-rata Semester 2 (0–20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu2_no_eval = st.number_input("Mata Kuliah Tanpa Evaluasi (Sem. 2)", min_value=0, max_value=20, value=0,
                                   help="Jumlah mata kuliah yang tidak mengikuti evaluasi")

st.divider()
st.subheader("Kondisi Ekonomi Makro (Saat Siswa Terdaftar)")
col9, col10 = st.columns(2)
with col9:
    unemployment_rate = st.number_input("Tingkat Pengangguran (%)", min_value=0.0, max_value=25.0, value=11.1, step=0.1,
                                         help="Persentase tingkat pengangguran nasional saat siswa mendaftar")
    inflation_rate = st.number_input("Tingkat Inflasi (%)", min_value=-5.0, max_value=10.0, value=1.4, step=0.1,
                                      help="Persentase inflasi nasional saat siswa mendaftar")
with col10:
    gdp = st.number_input("Pertumbuhan GDP (%)", min_value=-5.0, max_value=5.0, value=1.74, step=0.01,
                           help="Pertumbuhan ekonomi (GDP) nasional saat siswa mendaftar")

if st.button("🔍 Prediksi Risiko Dropout", type="primary", use_container_width=True):
    # build input dict sesuai urutan feature_names dari model
    input_data = {
        'Marital_status': marital_status,
        'Application_mode': application_mode,
        'Application_order': application_order,
        'Course': course,
        'Daytime_evening_attendance': daytime_evening,
        'Previous_qualification': previous_qualification,
        'Previous_qualification_grade': prev_qual_grade,
        'Nacionality': nacionality,
        'Mothers_qualification': mothers_qualification,
        'Fathers_qualification': fathers_qualification,
        'Mothers_occupation': mothers_occupation,
        'Fathers_occupation': fathers_occupation,
        'Admission_grade': admission_grade,
        'Displaced': displaced,
        'Educational_special_needs': educational_special_needs,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_fees,
        'Gender': gender,
        'Scholarship_holder': scholarship,
        'Age_at_enrollment': age_at_enrollment,
        'International': international,
        'Curricular_units_1st_sem_credited': cu1_credited,
        'Curricular_units_1st_sem_enrolled': cu1_enrolled,
        'Curricular_units_1st_sem_evaluations': cu1_evaluations,
        'Curricular_units_1st_sem_approved': cu1_approved,
        'Curricular_units_1st_sem_grade': cu1_grade,
        'Curricular_units_1st_sem_without_evaluations': cu1_no_eval,
        'Curricular_units_2nd_sem_credited': cu2_credited,
        'Curricular_units_2nd_sem_enrolled': cu2_enrolled,
        'Curricular_units_2nd_sem_evaluations': cu2_evaluations,
        'Curricular_units_2nd_sem_approved': cu2_approved,
        'Curricular_units_2nd_sem_grade': cu2_grade,
        'Curricular_units_2nd_sem_without_evaluations': cu2_no_eval,
        'Unemployment_rate': unemployment_rate,
        'Inflation_rate': inflation_rate,
        'GDP': gdp,
    }

    input_df = pd.DataFrame([input_data])[feature_names]
    proba = model.predict_proba(input_df)[0][1]
    pred = model.predict(input_df)[0]

    st.divider()
    st.subheader("Hasil Prediksi")

    if pred == 1:
        st.error(f"⚠️ **BERISIKO DROPOUT** — Probabilitas: {proba*100:.1f}%")
        st.markdown("""
        **Rekomendasi:**
        - Segera hubungi siswa untuk konseling akademik
        - Cek status pembayaran SPP dan pertimbangkan bantuan finansial
        - Pantau kehadiran dan partisipasi di kelas
        - Berikan bimbingan khusus untuk meningkatkan nilai
        """)
    else:
        st.success(f"✅ **TIDAK BERISIKO DROPOUT** — Probabilitas Dropout: {proba*100:.1f}%")
        st.markdown("""
        **Catatan:**
        - Siswa tampak stabil secara akademik
        - Tetap pantau secara berkala
        """)

    # progress bar probabilitas
    st.markdown(f"**Tingkat Risiko Dropout: {proba*100:.1f}%**")
    st.progress(float(proba))

st.divider()
st.caption("Sistem ini menggunakan model Random Forest yang dilatih pada data siswa Dropout dan Graduate dari dataset Jaya Jaya Institut. | Dibuat oleh Silvio Christian Joe")
