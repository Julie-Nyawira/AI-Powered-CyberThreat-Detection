# AI-Powered-CyberThreat-Detection
# AI-Powered Cyber Threat Detection Using Machine Learning on Network Traffic Data

## 1. Business Understanding

Cybersecurity threats are increasing rapidly in both frequency and sophistication. Traditional rule-based Intrusion Detection Systems (IDS) struggle to detect novel or zero-day attacks and are prone to generating excessive false negatives. Given the growing complexity of network traffic and threat vectors, organizations need intelligent, real-time solutions.

**Objective**: Build an AI-powered IDS that classifies and detects various cyber threats using machine learning, providing interpretability and real-time responsiveness.

According to Cybersecurity Ventures, global cybercrime damages are expected to reach **$10.5 trillion annually by 2025**, making proactive and intelligent cybersecurity systems essential for sectors like healthcare, finance, and critical infrastructure.

## 2. Objectives

- Explore the distribution of attack types to understand their frequency and severity.
- Train supervised machine learning models to classify normal and malicious traffic.
- Detect unknown threats (zero-day attacks) using anomaly detection techniques.
- Provide clear, interpretable insights using **LIME** for model predictions.
- Simulate real-time detection with stream-based tools for a production-ready IDS.

## 3. Data Understanding

- **Dataset**: UNSW-NB15
- **Source**: Australian Centre for Cyber Security (ACCS), UNSW Canberra
- **Total Records**: 2,540,044
- **Training Samples**: 175,341
- **Testing Samples**: 82,332
- **Attack Classes (9)**: DoS, Exploits, Reconnaissance, Shellcode, Fuzzers, Analysis, Backdoors, Generic, Worms
- **Normal Traffic**: 1 class
- **Total Final Features Used**: 42

## 4. Data Preparation

- Dropped Non-Generalizable Features: IPs, ports, timestamps (e.g., `saddr`, `stime`)
- Encoding: One-hot encoding for `proto`, `state`, `service`
- Scaling: StandardScaler applied to numerical features
- Class Imbalance: Addressed using class weights and stratified sampling
- Split Strategy: Training (70%), Validation (30%)

## 5. Modeling

### Unsupervised Learning

| Model              | Performance Summary |
|-------------------|---------------------|
| Isolation Forest  | Performed moderately well but affected by high contamination (48%) |
| One-Class SVM     | Underperformed due to rare anomaly assumption and imbalance |

### Supervised Learning

| Model              | Performance Summary |
|-------------------|---------------------|
| Logistic Regression | Solid baseline with decent recall |
| XGBoost (Untuned)   | Strong generalization, low false negatives |
| XGBoost (Tuned)     | Best overall model — high recall, balanced performance |
| Neural Network (MLP)| Stable training, good recall, no overfitting observed |

## 6. Evaluation & Interpretation

- **Metrics Used**: Accuracy, Precision, **Recall (primary)**, F1 Score, Confusion Matrix
- **Best Model**: Tuned XGBoost
- **LIME Interpretability**:
  - Features like `ct_state_ttl`, `state_CON`, and `ct_dst_sport_ltm` were most influential
  - Strong diagonal values in the confusion matrix, especially for high-frequency classes

## 7. Real-Time Simulation (Planned)

- Deployment Tools: Streamlit or FastAPI
- Real-time simulation via replayed `.pcap` files or streaming tools like River

### Example Threat Response Strategies:
- Fuzzers → Block IP
- Reconnaissance → Redirect to honeypots
- Worms → Disconnect infected host

## 8. Limitations

1. **Class Imbalance**: Low support for classes like Worms and Backdoors
2. **Anomaly Detection Challenges**: High contamination ratio limits detection efficiency
3. **Feature Context Loss**: Removing IPs and ports reduced forensic detail
4. **No Adversarial Testing**


## 9. Conclusions

- Supervised models outperformed unsupervised methods
- Tuned XGBoost achieved the best trade-off between generalization and recall
- LIME boosted model transparency for cybersecurity professionals
- Low-frequency attacks remain a challenge

## 10. Recommendations

1. Use **SMOTE** to balance class distribution.
2. Expand interpretability with **SHAP**.
3. Finalize streaming integration with River or Kafka.
4. Try ensemble learning (XGBoost + Neural Net).
5. Add automated mitigation (e.g., IP blocking) in deployment.