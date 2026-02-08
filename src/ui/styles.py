import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    /* ---------------- FONT ---------------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }


    /* ---------------- MAIN CARD ---------------- */
    .card {
        font-family: 'Inter', sans-serif !important;
        background: #ffffff !important;
        padding: 35px !important;
        border-radius: 18px !important;

        /* Stronger shadow */
        box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;

        /* Prevent full-width stretching */
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    .card b {
        color: #111827 !important;
    }

    /* ---------------- HEADINGS ---------------- */
    .card h1 {
        font-size: 34px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        margin-bottom: 12px !important;
    }


    /* ---------------- PARAGRAPHS ---------------- */
    .card p {
        font-size: 16px !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        color: #374151 !important;
        margin: 8px 0 !important;
    }

    
    /* ---------------- HR LINE ---------------- */
    .card hr {
        border: none !important;
        height: 1px !important;
        background: #e5e7eb !important;
        margin: 18px 0 !important;
    }


    /* ---------------- FOOTER TEXT ---------------- */
    .footer-text {
        margin-top: 35px !important;
        text-align: center !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #9ca3af !important;
    }


    /* ---------------- BUTTONS ---------------- */
    div.stButton > button {
        width: 100% !important;
        border-radius: 14px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }

    </style>
    """, unsafe_allow_html=True)
