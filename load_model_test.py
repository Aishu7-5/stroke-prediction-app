from tensorflow import keras

# Load model
model = keras.models.load_model("stroke_prediction_model.h5")
print("Model loaded successfully!")

# Optional: test with random input
import numpy as np
sample_input = np.random.rand(1, 10)  # 10 features
prediction = model.predict(sample_input)
print("Sample prediction:", prediction)
