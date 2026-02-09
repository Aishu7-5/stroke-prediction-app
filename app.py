import streamlit as st
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense

st.set_page_config(page_title="Stroke Prediction", layout="centered")

st.title("💓 Cardiovascular Stroke Prediction")
st.write("Select patient details to assess stroke risk")

# Cache the model loading to avoid reloading on every run
@st.cache_resource
def load_model():
    class CustomDense(Dense):
        def __init__(self, *args, **kwargs):
            kwargs.pop('quantization_config', None)
            super().__init__(*args, **kwargs)
    
    try:
        with keras.utils.custom_object_scope({'Dense': CustomDense}):
            model = keras.models.load_model("stroke_prediction_model.h5", compile=False)
        return model, None
    except Exception as e:
        return None, str(e)

# Load model
model, error = load_model()

if error:
    st.error(f"Failed to load model: {error}")
    st.stop()

# Form inputs with unique keys
gender = st.selectbox("Gender", ["Female", "Male", "Other"], key="gender")
gender_val = {"Female": 0, "Male": 1, "Other": 2}[gender]

age = st.number_input("Age", min_value=1, max_value=120, value=45, key="age")

hypertension = st.selectbox("Hypertension", ["No", "Yes"], key="hypertension")
hypertension_val = {"No": 0, "Yes": 1}[hypertension]

heart_disease = st.selectbox("Heart Disease", ["No", "Yes"], key="heart_disease")
heart_disease_val = {"No": 0, "Yes": 1}[heart_disease]

avg_glucose_level = st.number_input(
    "Average Glucose Level (mg/dL)", min_value=50.0, max_value=300.0, value=95.0, key="glucose"
)

bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0, key="bmi")

ever_married = st.selectbox("Ever Married", ["No", "Yes"], key="married")
ever_married_val = {"No": 0, "Yes": 1}[ever_married]

work_type = st.selectbox(
    "Work Type",
    ["Government Job", "Private Job", "Self-employed", "Children", "Never worked"],
    key="work_type"
)
work_type_val = {
    "Government Job": 0,
    "Private Job": 1,
    "Self-employed": 2,
    "Children": 3,
    "Never worked": 4
}[work_type]

residence = st.selectbox("Residence Type", ["Rural", "Urban"], key="residence")
residence_val = {"Rural": 0, "Urban": 1}[residence]

smoking = st.selectbox(
    "Smoking Status",
    ["Never smoked", "Formerly smoked", "Smokes", "Unknown"],
    key="smoking"
)
smoking_val = {
    "Formerly smoked": 0,
    "Never smoked": 1,
    "Smokes": 2,
    "Unknown": 3
}[smoking]

# Prediction button
if st.button("Predict Stroke Risk", key="predict_btn"):
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
    prediction = model.predict(input_data, verbose=0)
    prob_percent = prediction[0][0] * 100

    st.write(f"### Stroke Probability: **{prob_percent:.2f}%**")

    # Risk assessment
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
        if prob_percent < 30:
            st.success("🟢 Low Risk of Stroke (Normal)")
        elif prob_percent < 60:
            st.warning("🟡 Moderate Risk of Stroke (Borderline)")
        else:
            st.error("🔴 High Risk of Stroke")

# Footer
st.markdown("---")
st.caption("⚠️ This prediction is for educational purposes only and not a medical diagnosis.")

