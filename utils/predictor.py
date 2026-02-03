import numpy as np

def predict(model, features):
    probs = model.predict_proba([features])[0]
    confidence = float(max(probs))

    label = "AI_GENERATED" if np.argmax(probs) == 1 else "HUMAN"
    return label, confidence
