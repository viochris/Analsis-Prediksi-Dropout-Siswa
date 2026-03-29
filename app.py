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
                                   format_func=lambda x: {1:'Single', 2:'Married', 3:'Widower',
                                                          4:'Divorced', 5:'Facto Union', 6:'Legally Separated'}[x])
    gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: 'Male' if x==1 else 'Female')
    age_at_enrollment = st.number_input("Usia saat Mendaftar", min_value=17, max_value=70, value=20)
    
    nacionality_dict = {
        1: 'Portuguese', 2: 'German', 6: 'Spanish', 11: 'Italian', 13: 'Dutch',
        14: 'English', 17: 'Lithuanian', 21: 'Angolan', 22: 'Cape Verdean',
        24: 'Guinean', 25: 'Mozambican', 26: 'Santomean', 32: 'Turkish',
        41: 'Brazilian', 62: 'Romanian', 100: 'Moldova (Republic of)',
        101: 'Mexican', 103: 'Ukrainian', 105: 'Russian', 108: 'Cuban', 109: 'Colombian'
    }
    nacionality = st.selectbox("Nasionalitas", 
                               options=list(nacionality_dict.keys()), 
                               format_func=lambda x: nacionality_dict[x])
                               
    displaced = st.selectbox("Displaced (tinggal jauh dari rumah)?", options=[0, 1],
                              format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    international = st.selectbox("Mahasiswa Internasional?", options=[0, 1],
                                  format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    educational_special_needs = st.selectbox("Kebutuhan Pendidikan Khusus?", options=[0, 1],
                                              format_func=lambda x: 'Ya' if x==1 else 'Tidak')

with col2:
    st.markdown("**Informasi Akademik & Keuangan**")
    course = st.selectbox("Program Studi",
                           options=[33, 171, 8014, 9003, 9070, 9085, 9119, 9130,
                                    9147, 9238, 9254, 9500, 9556, 9670, 9773, 9853, 9991],
                           format_func=lambda x: {
                               33:'Biofuel Production Technologies', 171:'Animation & Multimedia Design',
                               8014:'Social Service (Evening)', 9003:'Agronomy', 9070:'Communication Design',
                               9085:'Veterinary Nursing', 9119:'Informatics Engineering', 9130:'Equinculture',
                               9147:'Management', 9238:'Social Service', 9254:'Tourism', 9500:'Nursing',
                               9556:'Oral Hygiene', 9670:'Advertising & Marketing Management',
                               9773:'Journalism & Communication', 9853:'Basic Education',
                               9991:'Management (Evening)'
                           }[x])
    daytime_evening = st.selectbox("Jenis Kelas", options=[1, 0],
                                    format_func=lambda x: 'Pagi/Siang' if x==1 else 'Malam')
                                    
    app_mode_dict = {
        1: '1st phase - general contingent', 2: 'Ordinance No. 612/93', 5: '1st phase - special contingent (Azores Island)',
        7: 'Holders of other higher courses', 10: 'Ordinance No. 854-B/99', 15: 'International student (bachelor)',
        16: '1st phase - special contingent (Madeira Island)', 17: '2nd phase - general contingent', 18: '3rd phase - general contingent',
        26: 'Ordinance No. 533-A/99, item b2) (Different Plan)', 27: 'Ordinance No. 533-A/99, item b3 (Other Institution)',
        39: 'Over 23 years old', 42: 'Transfer', 43: 'Change of course', 44: 'Technological specialization diploma holders',
        51: 'Change of institution/course', 53: 'Short cycle diploma holders', 57: 'Change of institution/course (International)'
    }
    application_mode = st.selectbox("Mode Aplikasi Masuk", 
                                    options=list(app_mode_dict.keys()), 
                                    format_func=lambda x: app_mode_dict[x],
                                    index=7) # Default ke 17 (2nd phase)

    application_order = st.selectbox("Urutan Pilihan Program", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                     format_func=lambda x: f"Pilihan ke-{x}" if x > 0 else "Pilihan ke-0 (Pertama)")
    
    prev_qual_dict = {
        1: 'Secondary education', 2: "Higher education - bachelor's degree", 3: 'Higher education - degree',
        4: "Higher education - master's", 5: 'Higher education - doctorate', 6: 'Frequency of higher education',
        9: '12th year of schooling - not completed', 10: '11th year of schooling - not completed',
        12: 'Other - 11th year of schooling', 14: '10th year of schooling', 15: '10th year of schooling - not completed',
        19: 'Basic education 3rd cycle (9th/10th/11th year) or equiv.', 38: 'Basic education 2nd cycle (6th/7th/8th year) or equiv.',
        39: 'Technological specialization course', 40: 'Higher education - degree (1st cycle)',
        42: 'Professional higher technical course', 43: 'Higher education - master (2nd cycle)'
    }
    previous_qualification = st.selectbox("Kualifikasi Sebelumnya", 
                                          options=list(prev_qual_dict.keys()), 
                                          format_func=lambda x: prev_qual_dict[x])

    prev_qual_grade = st.slider("Nilai Kualifikasi Sebelumnya (0-200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    admission_grade = st.slider("Nilai Masuk (0-200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    tuition_fees = st.selectbox("Bayar SPP Tepat Waktu?", options=[1, 0],
                                 format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    debtor = st.selectbox("Memiliki Hutang?", options=[0, 1],
                          format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    scholarship = st.selectbox("Penerima Beasiswa?", options=[0, 1],
                                format_func=lambda x: 'Ya' if x==1 else 'Tidak')

st.markdown("**Informasi Orang Tua**")
col3, col4 = st.columns(2)
with col3:
    mothers_qualification = st.number_input("Kualifikasi Ibu (kode)", min_value=1, max_value=44, value=19,
                                             help="Lihat dokumentasi dataset untuk daftar kode kualifikasi")
    mothers_occupation = st.number_input("Pekerjaan Ibu (kode)", min_value=0, max_value=194, value=5,
                                          help="Lihat dokumentasi dataset untuk daftar kode pekerjaan")
with col4:
    fathers_qualification = st.number_input("Kualifikasi Ayah (kode)", min_value=1, max_value=44, value=19,
                                            help="Lihat dokumentasi dataset untuk daftar kode kualifikasi")
    fathers_occupation = st.number_input("Pekerjaan Ayah (kode)", min_value=0, max_value=194, value=5,
                                         help="Lihat dokumentasi dataset untuk daftar kode pekerjaan")

st.divider()
st.subheader("Performa Semester 1")
col5, col6 = st.columns(2)

with col5:
    cu1_credited = st.number_input("Unit Credited Sem. 1", min_value=0, max_value=20, value=0)
    cu1_enrolled = st.number_input("Unit Terdaftar Sem. 1", min_value=0, max_value=30, value=6)
    cu1_evaluations = st.number_input("Evaluasi Sem. 1", min_value=0, max_value=40, value=6)

with col6:
    cu1_approved = st.number_input("Unit Lulus Sem. 1", min_value=0, max_value=30, value=5)
    cu1_grade = st.slider("Nilai Rata-rata Sem. 1 (0-20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu1_no_eval = st.number_input("Unit Tanpa Evaluasi Sem. 1", min_value=0, max_value=20, value=0)

st.subheader("Performa Semester 2")
col7, col8 = st.columns(2)

with col7:
    cu2_credited = st.number_input("Unit Credited Sem. 2", min_value=0, max_value=20, value=0)
    cu2_enrolled = st.number_input("Unit Terdaftar Sem. 2", min_value=0, max_value=30, value=6)
    cu2_evaluations = st.number_input("Evaluasi Sem. 2", min_value=0, max_value=40, value=6)

with col8:
    cu2_approved = st.number_input("Unit Lulus Sem. 2", min_value=0, max_value=30, value=5)
    cu2_grade = st.slider("Nilai Rata-rata Sem. 2 (0-20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu2_no_eval = st.number_input("Unit Tanpa Evaluasi Sem. 2", min_value=0, max_value=20, value=0)

st.divider()
st.subheader("Kondisi Ekonomi Makro")
col9, col10 = st.columns(2)
with col9:
    unemployment_rate = st.number_input("Tingkat Pengangguran (%)", min_value=0.0, max_value=25.0, value=11.1, step=0.1)
    inflation_rate = st.number_input("Tingkat Inflasi (%)", min_value=-5.0, max_value=10.0, value=1.4, step=0.1)
with col10:
    gdp = st.number_input("GDP", min_value=-5.0, max_value=5.0, value=1.74, step=0.01)

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