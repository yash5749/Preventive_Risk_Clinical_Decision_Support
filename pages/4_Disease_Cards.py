import streamlit as st
from src.core.risk_utils import SUPPORTED_DISEASES, get_features_for_disease

st.set_page_config(
    page_title="Disease Screening Cards",
    layout="wide"
)

st.title("🩺 Multi-Disease Preventive Screening")
st.caption("OPD-grade early risk screening • Click a disease to begin")

st.divider()

# ---------------- SESSION STATE ----------------
if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = None

# ---------------- DISEASE CARDS ----------------
st.subheader("📋 Select Disease")

# Add card CSS once (uses your existing Inter font)
st.markdown("""
<style>
.disease-card {
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    transition: all 0.25s ease;
    min-height: 150px;
}

.disease-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    border-color: #2563eb;
}

.disease-card h3 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #111827;
}

.disease-card p {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(4)

diseases = [
    ("diabetes", "🩸 Diabetes", "Blood sugar & metabolic risk"),
    ("hypertension", "❤️ Hypertension", "Cardiovascular pressure risk"),
    ("thyroid", "🦋 Thyroid", "Hormonal imbalance screening"),
    ("kidney", "🫘 Kidney", "Renal function & filtration risk"),
]

for col, (key, title, desc) in zip(cols, diseases):
    with col:
        # Card UI
        st.markdown(
            f"""
            <div class="disease-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Clean button
        if st.button("Start Screening", key=key):
            st.session_state.selected_disease = key
            st.rerun()


st.divider()

# ---------------- DYNAMIC FORM ----------------
if st.session_state.selected_disease:

    disease = st.session_state.selected_disease
    st.subheader(f"🧾 {disease.capitalize()} Screening Form")

    features = get_features_for_disease(disease)

    input_data = {}

    cols = st.columns(3)

    for i, feature in enumerate(features):
        with cols[i % 3]:
            if feature in ["gender", "smoking_history"]:
                options = ["Male", "Female"] if feature == "gender" else ["never", "former", "current"]
                input_data[feature] = st.selectbox(feature.replace("_", " ").title(), options)

            elif feature in ["hypertension", "heart_disease"]:
                input_data[feature] = st.selectbox(
                    feature.replace("_", " ").title(),
                    [0, 1],
                    format_func=lambda x: "Yes" if x == 1 else "No"
                )

            else:
                input_data[feature] = st.number_input(
                    feature.replace("_", " ").title(),
                    min_value=0.0
                )

    st.info("Prediction & explanation will appear in next phase")

else:
    st.info("⬆️ Select a disease card to start screening")
