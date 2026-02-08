import streamlit as st
from .styles import apply_styles

apply_styles()

def landing_page():
    st.markdown("""
    <div class="card">
        <h1 style="text-align:center;">🩺 Preventive Diabetes Risk Assessment</h1>
        <p style="text-align:center;">
            Early screening & AI-assisted clinical decision support
        </p>
        <hr>
        <p style="text-align:center;">
            This tool helps assess diabetes risk using basic health indicators.<br>
            It is intended for <b>screening & preventive care only</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧍 Patient Assessment"):
            st.session_state.page = "Patient Assessment"
            st.rerun()

    with col2:
        if st.button("👨‍⚕️ Doctor Login"):
            st.session_state.page = "Doctor Login"
            st.rerun()

    st.markdown("""
    <div class="footer-text">
        ⚠️ This is not a medical diagnosis. Always consult a qualified doctor.
    </div>
    """, unsafe_allow_html=True)
