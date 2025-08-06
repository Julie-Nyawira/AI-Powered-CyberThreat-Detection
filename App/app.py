import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- Load model and encoder ---
model = joblib.load("model.pkl")
class_names = joblib.load("class_names.pkl")  # e.g., ['Normal', 'DoS', 'Reconnaissance', ...]

# --- Mapping: attack category ➝ response action ---
response_actions = {
    "Fuzzers": "Immediately block the source IP",
    "Analysis": "Trigger anomaly alerts on repeated or fast port scans.",
    "Backdoors": "Isolate the affected host from the network.",
    "DoS": "Rate-limit or temporarily blacklist attack IPs.",
    "Exploits": "Log and contain affected systems.",
    "Generic": "Temporarily lock user accounts after failed attempts.",
    "Reconnaissance": "Redirect to honeypots or dummy services.",
    "Shellcode": "Reimage or restore from a known good backup.",
    "Worms": "Disconnect infected systems immediately.",
    "Normal": "No action required. Normal traffic."
}

# --- Streamlit UI setup ---
st.set_page_config(page_title="UNSW-NB15 Attack Category Predictor")
st.title("🔒 UNSW-NB15 Attack Category Predictor")
st.markdown("Upload a CSV file with network traffic features to predict attack categories and receive recommended responses.")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)

        st.subheader("📄 Uploaded Data (First 5 Rows)")
        st.dataframe(data.head())

        # --- Make predictions ---
        try:
            preds = model.predict(data)
            pred_labels = [class_names[p] for p in preds]
            actions = [response_actions.get(label, "No action defined.") for label in pred_labels]

            # Combine results
            results = data.copy()
            results["Predicted Attack Category"] = pred_labels
            results["Recommended Response"] = actions

            # --- Show results ---
            st.subheader("🔍 Prediction Results with Recommended Actions")
            st.dataframe(results)

            # --- Allow download ---
            csv = results.to_csv(index=False).encode()
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="attack_predictions.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")

    except Exception as e:
        st.error(f"❌ Failed to read CSV file: {e}")
