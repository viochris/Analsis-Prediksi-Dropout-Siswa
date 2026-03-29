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
    displaced = st.selectbox("Displaced (tinggal jauh dari rumah)?", options=[0, 1], 
                              format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    international = st.selectbox("Mahasiswa Internasional?", options=[0, 1],
                                  format_func=lambda x: 'Ya' if x==1 else 'Tidak')

with col2:
    st.markdown("**Informasi Akademik & Keuangan**")
    admission_grade = st.slider("Nilai Masuk (0-200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    prev_qual_grade = st.slider("Nilai Kualifikasi Sebelumnya (0-200)", min_value=0.0, max_value=200.0, value=130.0, step=0.5)
    tuition_fees = st.selectbox("Bayar SPP Tepat Waktu?", options=[1, 0], 
                                 format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    debtor = st.selectbox("Memiliki Hutang?", options=[0, 1], 
                          format_func=lambda x: 'Ya' if x==1 else 'Tidak')
    scholarship = st.selectbox("Penerima Beasiswa?", options=[0, 1],
                                format_func=lambda x: 'Ya' if x==1 else 'Tidak')

st.divider()
st.subheader("Performa Semester 1")
col3, col4 = st.columns(2)

with col3:
    cu1_enrolled = st.number_input("Unit Terdaftar Sem. 1", min_value=0, max_value=30, value=6)
    cu1_evaluations = st.number_input("Evaluasi Sem. 1", min_value=0, max_value=40, value=6)
    cu1_approved = st.number_input("Unit Lulus Sem. 1", min_value=0, max_value=30, value=5)

with col4:
    cu1_grade = st.slider("Nilai Rata-rata Sem. 1 (0-20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu1_credited = st.number_input("Unit Credited Sem. 1", min_value=0, max_value=20, value=0)
    cu1_no_eval = st.number_input("Unit Tanpa Evaluasi Sem. 1", min_value=0, max_value=20, value=0)

st.subheader("Performa Semester 2")
col5, col6 = st.columns(2)

with col5:
    cu2_enrolled = st.number_input("Unit Terdaftar Sem. 2", min_value=0, max_value=30, value=6)
    cu2_evaluations = st.number_input("Evaluasi Sem. 2", min_value=0, max_value=40, value=6)
    cu2_approved = st.number_input("Unit Lulus Sem. 2", min_value=0, max_value=30, value=5)

with col6:
    cu2_grade = st.slider("Nilai Rata-rata Sem. 2 (0-20)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    cu2_credited = st.number_input("Unit Credited Sem. 2", min_value=0, max_value=20, value=0)
    cu2_no_eval = st.number_input("Unit Tanpa Evaluasi Sem. 2", min_value=0, max_value=20, value=0)

st.divider()

# Nilai default untuk fitur yang tidak ditampilkan di form
default_values = {
    'Application_mode': 17,
    'Application_order': 1,
    'Course': 9147,
    'Daytime_evening_attendance': 1,
    'Previous_qualification': 1,
    'Nacionality': 1,
    'Mothers_qualification': 19,
    'Fathers_qualification': 19,
    'Mothers_occupation': 5,
    'Fathers_occupation': 5,
    'Educational_special_needs': 0,
    'Unemployment_rate': 11.1,
    'Inflation_rate': 1.4,
    'GDP': 1.74
}

if st.button("🔍 Prediksi Risiko Dropout", type="primary", use_container_width=True):
    # build input dict
    input_data = {
        'Marital_status': marital_status,
        'Application_mode': default_values['Application_mode'],
        'Application_order': default_values['Application_order'],
        'Course': default_values['Course'],
        'Daytime_evening_attendance': default_values['Daytime_evening_attendance'],
        'Previous_qualification': default_values['Previous_qualification'],
        'Previous_qualification_grade': prev_qual_grade,
        'Nacionality': default_values['Nacionality'],
        'Mothers_qualification': default_values['Mothers_qualification'],
        'Fathers_qualification': default_values['Fathers_qualification'],
        'Mothers_occupation': default_values['Mothers_occupation'],
        'Fathers_occupation': default_values['Fathers_occupation'],
        'Admission_grade': admission_grade,
        'Displaced': displaced,
        'Educational_special_needs': default_values['Educational_special_needs'],
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
        'Unemployment_rate': default_values['Unemployment_rate'],
        'Inflation_rate': default_values['Inflation_rate'],
        'GDP': default_values['GDP'],
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
st.caption("Sistem ini menggunakan model Random Forest yang dilatih pada dataset Jaya Jaya Institut. | Dibuat oleh Silvio Christian Joe")
