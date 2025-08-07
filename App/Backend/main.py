from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI backend for the AI model is up and running!"}


# Allow Streamlit (running separately) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and class labels
model = joblib.load("model.pkl")
class_names = joblib.load("class_names.pkl")

# Mapping attack → response
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

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read file content
    df = pd.read_csv(io.BytesIO(await file.read()))
    preds = model.predict(df)
    labels = [class_names[p] for p in preds]
    actions = [response_actions.get(label, "No action defined.") for label in labels]

    df["Predicted Attack Category"] = labels
    df["Recommended Response"] = actions

    return df.to_dict(orient="records")

