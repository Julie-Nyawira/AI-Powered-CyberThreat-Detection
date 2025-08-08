import streamlit as st
import os
import base64
import random
import pandas as pd
import requests

st.set_page_config(page_title="Hybrid UNSW-NB15 Predictor", layout = "wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        /* Transparent panels */
        .block-container {{
            background-color: rgba(0, 0, 0, 0.88);
            padding: 2rem;
            border-radius: 10px;
        }}
        /* Neon text */
        h1, h2, h3, p, label {{
            color: #00FF41 !important;
            font-family: 'Courier New', monospace;
        }}
        /* Table style */
        .dataframe {{
            color: #00FF41 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Get all image files from assets
image_folder = "assets"
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg", ".webp"))]

# Pick one at random
selected_image = random.choice(images)
add_bg_from_local(selected_image)



st.title("🔄 AI-Powered Cyber Threat Detection App")
st.markdown("Upload a CSV to get cyber-attack predictions and recommended responses")

uploaded_file = st.file_uploader("Upload Network Log CSV File", type=["csv"])

if uploaded_file:
    st.subheader("📄 Uploaded Data (First 5 Rows)")
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

    # Prepare file for FastAPI
    file_bytes = uploaded_file.getvalue()
    files = {"file": (uploaded_file.name, file_bytes, "text/csv")}

    try:
        with st.spinner("Analyzing network traffic..."):
            response = requests.post("http://localhost:8000/predict", files=files)

            if response.status_code == 200:
                results = pd.DataFrame(response.json())
                st.success("✅ Prediction received!")
                st.dataframe(results)

                import plotly.express as px

                # Visualize only if results exist
                if not results.empty:
                    st.subheader("📊 Distribution of Detected Cyber Threats")

                    # Value counts
                    attack_counts = results["Predicted Attack Category"].value_counts().reset_index()
                    attack_counts.columns = ["Attack Category", "Count"]

                    # 📊 Bar Chart
                    fig_bar = px.bar(
                        attack_counts,
                        x="Attack Category",
                        y="Count",
                        title="📊 Attack Category Distribution",
                        labels={"Count": "Number of Records"},
                        text_auto=True,
                        template="plotly_dark",
                        color="Attack Category",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig_bar.update_layout(
                    plot_bgcolor="#000000",
                    paper_bgcolor="#000000",
                    font=dict(color="#00FF41")
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True)


                    # 🥧 Pie Chart
                    st.subheader("🥧 Attack Category Percentage Breakdown")
                    fig_pie = px.pie(
                        attack_counts,
                        names="Attack Category",
                        values="Count",
                        title="🔍 Attack Category Percentages",
                        hole=0.4,  # For a donut-style pie chart
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig_pie.update_layout(
                    plot_bgcolor="#000000",
                    paper_bgcolor="#000000",
                    font=dict(color="#00FF41")
                    )

                    st.plotly_chart(fig_pie, use_container_width=True)

                st.subheader("📜 Summary of Recommended Responses")

                # Group by Attack Category & Recommended Response
                summary_df = results.groupby(["Predicted Attack Category", "Recommended Response"]).size().reset_index(name="Count")
 
                summary_df = summary_df[["Predicted Attack Category", "Count", "Recommended Response"]]

                # Show table
                st.dataframe(summary_df, hide_index = True)
                

                csv = results.to_csv(index=False).encode()
                st.download_button("Download CSV", data=csv, file_name="hybrid_predictions.csv", mime="text/csv")
                
            else:
                st.error(f"❌ FastAPI error: {response.status_code}\nDetails: {response.text}")
    except Exception as e:
        st.error(f"❌ Could not connect to FastAPI: {e}")
