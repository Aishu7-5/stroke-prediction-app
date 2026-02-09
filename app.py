import streamlit as st
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense

# Model Loading Fix: Handle 'quantization_config' error in newer Keras versions
class CustomDense(Dense):
    def __init__(self, *args, **kwargs):
        # Strip the unrecognized argument if present
        kwargs.pop('quantization_config', None)
        super().__init__(*args, **kwargs)

# Load trained model with custom object scope and compile=False (safer for inference)
try:
    with keras.utils.custom_object_scope({'Dense': CustomDense}):
        model = keras.models.load_model("stroke_prediction_model.h5", compile=False)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    # Fallback/Stop to avoid crash loop
    st.stop()

st.title("💓 Cardiovascular Stroke Prediction")
st.write("Select patient details to assess stroke risk")

# ---------------- INPUTS (WORDS ONLY) ----------------
gender = st.selectbox("Gender", ["Female", "Male", "Other"])
gender_val = {"Female": 0, "Male": 1, "Other": 2}[gender]

age = st.number_input("Age", min_value=1, max_value=120, value=45)

hypertension = st.selectbox("Hypertension", ["No", "Yes"])
hypertension_val = {"No": 0, "Yes": 1}[hypertension]

heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
heart_disease_val = {"No": 0, "Yes": 1}[heart_disease]

avg_glucose_level = st.number_input(
    "Average Glucose Level (mg/dL)", min_value=50.0, max_value=300.0, value=95.0
)

bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0)

ever_married = st.selectbox("Ever Married", ["No", "Yes"])
ever_married_val = {"No": 0, "Yes": 1}[ever_married]

work_type = st.selectbox(
    "Work Type",
    ["Government Job", "Private Job", "Self-employed", "Children", "Never worked"]
)
work_type_val = {
    "Government Job": 0,
    "Private Job": 1,
    "Self-employed": 2,
    "Children": 3,
    "Never worked": 4
}[work_type]

residence = st.selectbox("Residence Type", ["Rural", "Urban"])
residence_val = {"Rural": 0, "Urban": 1}[residence]

smoking = st.selectbox(
    "Smoking Status",
    ["Never smoked", "Formerly smoked", "Smokes", "Unknown"]
)
smoking_val = {
    "Formerly smoked": 0,
    "Never smoked": 1,
    "Smokes": 2,
    "Unknown": 3
}[smoking]

# ---------------- PREDICTION ----------------
if st.button("Predict Stroke Risk"):

    # Normalize input data
    input_data = np.array([[ 
        gender_val / 2,
        age / 100,
        hypertension_val,
        heart_disease_val,
        avg_glucose_level / 300,
        bmi / 60,
        ever_married_val,
        work_type_val / 4,
        residence_val,
        smoking_val / 3
    ]])

    # Model prediction
    prediction = model.predict(input_data)
    prob_percent = prediction[0][0] * 100  # convert to percentage

    st.write(f"### Stroke Probability: **{prob_percent:.2f}%**")

    # -------- RULE-BASED OVERRIDE FOR CLEARLY HEALTHY CASES --------
    if (
        age < 50 and
        hypertension_val == 0 and
        heart_disease_val == 0 and
        avg_glucose_level < 110 and
        bmi < 25 and
        smoking == "Never smoked"
    ):
        st.success("🟢 Low Risk of Stroke (Normal)")
    else:
        # -------- SCIENTIFIC RISK BANDS --------
        if prob_percent < 30:
            st.success("🟢 Low Risk of Stroke (Normal)")
        elif prob_percent < 60:
            st.warning("🟡 Moderate Risk of Stroke (Borderline)")
        else:
            st.error("🔴 High Risk of Stroke")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ This prediction is for educational purposes only and not a medical diagnosis.")

