import streamlit as st
import pandas as pd
from ui.styles import apply_styles

from src.core.db import get_connection
from src.core.decision_support import next_steps
from src.core.genai_explainer import explain
from src.core.pdf_report import generate_pdf
from src.core.i18n import get_text

apply_styles()


def doctor_dashboard():

    # ===============================
    # LANGUAGE CONTEXT
    # ===============================
    lang = st.session_state.get("language", "English")
    T = get_text(lang)

    # ===============================
    # PAGE HEADER
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">👨‍⚕️ {T['dashboard']}</div>
        <p style="color:#6b7280">
            {"Clinical decision support & longitudinal patient monitoring"
             if lang == "English"
             else "क्लिनिकल निर्णय सहायता और रोगी निगरानी"}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===============================
    # LOAD DATA
    # ===============================
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM patient_records ORDER BY created_at DESC",
        conn
    )
    conn.close()

    if df.empty:
        st.info(
            "No patient records available yet."
            if lang == "English"
            else "अभी तक कोई रोगी रिकॉर्ड उपलब्ध नहीं है।"
        )
        return

    # ===============================
    # ALL PATIENT RECORDS
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">📋 {T['patient_records']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, width="stretch")

    # ===============================
    # SELECT PATIENT
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">🔍 
            {"Review Patient History" if lang == "English" else "रोगी का इतिहास देखें"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    patient_ids = df["patient_id"].unique().tolist()
    selected_patient = st.selectbox(T["select_patient"], patient_ids)

    patient_df = df[df["patient_id"] == selected_patient].sort_values("created_at")
    latest = patient_df.iloc[-1]

    # ===============================
    # RISK OVERVIEW CARD
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">📊 {T['risk_overview']}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(T["patient_id"], latest["patient_id"])
    with col2:
        st.metric(
            "Risk Probability" if lang == "English" else "जोखिम प्रतिशत",
            f"{latest['risk_probability']*100:.2f}%"
        )
    with col3:
        st.metric(T["risk_category"], latest["risk_category"])

    # ===============================
    # HISTORY & TRENDS
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">📈 {T['history_trends']}</div>
    </div>
    """, unsafe_allow_html=True)

    if len(patient_df) > 1:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                "**Diabetes Risk (%) Over Time**"
                if lang == "English"
                else "**समय के साथ डायबिटीज जोखिम (%)**"
            )
            st.line_chart(
                patient_df.set_index("created_at")["risk_probability"] * 100
            )

        with col2:
            st.markdown(
                "**HbA1c Trend Over Time**"
                if lang == "English"
                else "**HbA1c का ट्रेंड**"
            )
            st.line_chart(
                patient_df.set_index("created_at")["hba1c"]
            )

        st.markdown(
            "**BMI Trend Over Time**"
            if lang == "English"
            else "**BMI का ट्रेंड**"
        )
        st.line_chart(
            patient_df.set_index("created_at")["bmi"]
        )

    else:
        st.info(
            "Not enough historical data to show trends."
            if lang == "English"
            else "ट्रेंड दिखाने के लिए पर्याप्त डेटा उपलब्ध नहीं है।"
        )

    # ===============================
    # AI CLINICAL EXPLANATION
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">🤖 {T['ai_explanation']}</div>
    </div>
    """, unsafe_allow_html=True)

    patient_data = {
        "gender": latest["gender"],
        "age": latest["age"],
        "hypertension": latest["hypertension"],
        "heart_disease": latest["heart_disease"],
        "smoking_history": latest["smoking_history"],
        "bmi": latest["bmi"],
        "HbA1c_level": latest["hba1c"],
        "blood_glucose_level": latest["glucose"]
    }

    ai_explanation = explain(
        patient_data=patient_data,
        risk=latest["risk_category"],
        prob=latest["risk_probability"],
        audience="clinician"
    )

    st.write(ai_explanation)

    # ===============================
    # NEXT STEPS
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">🩺 {T['next_steps']}</div>
    </div>
    """, unsafe_allow_html=True)

    steps = next_steps(latest["risk_category"])
    for step in steps:
        st.write("•", step)

    # ===============================
    # PDF REPORT
    # ===============================
    st.markdown(f"""
    <div class="card">
        <div class="section-title">📄 
            {"Patient Report" if lang == "English" else "रोगी रिपोर्ट"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "📥 Generate & Download PDF Report"
        if lang == "English"
        else "📥 रिपोर्ट डाउनलोड करें",
        width="stretch"
    ):

        pdf_path = generate_pdf(
            latest.to_dict(),
            ai_explanation
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                label=T["download_pdf"],
                data=f,
                file_name=f"{latest['patient_id']}_report.pdf",
                mime="application/pdf"
            )

    st.caption(
        "⚠️ This dashboard provides clinical decision support only."
        if lang == "English"
        else "⚠️ यह डैशबोर्ड केवल क्लिनिकल निर्णय सहायता के लिए है।"
    )
