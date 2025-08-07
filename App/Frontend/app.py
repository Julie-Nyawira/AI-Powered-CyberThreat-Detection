import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Hybrid UNSW-NB15 Predictor")

st.title("🔄 Hybrid UNSW-NB15 Prediction App")
st.markdown("Upload a CSV to get attack category predictions and recommended responses via FastAPI.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    st.subheader("📄 Uploaded Data (First 5 Rows)")
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

    # Prepare file for FastAPI
    file_bytes = uploaded_file.getvalue()
    files = {"file": (uploaded_file.name, file_bytes, "text/csv")}

    try:
        with st.spinner("Sending data to FastAPI for prediction..."):
            response = requests.post("http://localhost:8000/predict", files=files)

            if response.status_code == 200:
                results = pd.DataFrame(response.json())
                st.success("✅ Prediction received!")
                st.dataframe(results)

                import plotly.express as px

                # Visualize only if results exist
                if not results.empty:
                    st.subheader("📊 Distribution of Predicted Attack Categories")

                    # Value counts
                    attack_counts = results["Predicted Attack Category"].value_counts().reset_index()
                    attack_counts.columns = ["Attack Category", "Count"]

                    # 📊 Bar Chart
                    fig_bar = px.bar(
                        attack_counts,
                        x="Attack Category",
                        y="Count",
                        title="Predicted Attack Category Distribution",
                        labels={"Count": "Number of Records"},
                        text_auto=True
                    )
                    st.plotly_chart(fig_bar)

                    # 🥧 Pie Chart
                    st.subheader("🥧 Attack Category Percentage Breakdown")
                    fig_pie = px.pie(
                        attack_counts,
                        names="Attack Category",
                        values="Count",
                        title="Attack Category Percentages",
                        hole=0.4  # For a donut-style pie chart
                    )
                    st.plotly_chart(fig_pie)
                    
                st.subheader("🛡️ Summary of Recommended Responses")
                summary_df = results.groupby("Recommended Response").size().reset_index(name="Count")
                st.dataframe(summary_df)


                csv = results.to_csv(index=False).encode()
                st.download_button("Download CSV", data=csv, file_name="hybrid_predictions.csv", mime="text/csv")
                
            else:
                st.error(f"❌ FastAPI error: {response.status_code}\nDetails: {response.text}")
    except Exception as e:
        st.error(f"❌ Could not connect to FastAPI: {e}")
