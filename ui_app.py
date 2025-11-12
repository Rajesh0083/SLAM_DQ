import streamlit as st
import pandas as pd
from utils.file_loader import load_file, save_output
import calendar
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Data Quality Checker", layout="centered")

st.title("📊 Data Quality Validation Tool")
st.markdown("Upload your dataset, select output folder, and run validation checks.")

# ========== USER INPUTS ==========

# Define provider options
provider_options = ["RHW", "RXQ", "RTH", "DEF", "GHI"]  # Add as many as you want
selected_provider = st.selectbox("🏢 Select Provider", provider_options)

# Define year options (e.g. from 2020 to current + 2)
current_year = datetime.now().year
year_options = list(range(2020, current_year + 3))
selected_year = st.selectbox("📅 Select Financial Year", sorted(year_options, reverse=True))

# Define month options
month_dict = {calendar.month_name[i]: i for i in range(1, 13)}
selected_month_name = st.selectbox("🗓️ Select Financial Month", list(month_dict.keys()))
selected_month = month_dict[selected_month_name]

st.markdown("---")

# File upload
uploaded_file = st.file_uploader("📁 Upload your dataset (Excel or CSV)", type=["xlsx", "csv"])

# Output folder path
output_folder = st.text_input(
    "📂 Enter output folder path (where report should be saved)",
    help="Example: C:\\Rajesh\\Personal\\DQ_Output\\RHW\\2025_09",
)

# ========== PROCESSING ==========
if uploaded_file and output_folder:
    try:
        df = load_file(uploaded_file)
        st.success(f"✅ File '{uploaded_file.name}' loaded successfully for provider {selected_provider}.")
        st.write("### 📋 Data Preview")
        st.dataframe(df.head(10))

        # Placeholder for rule validation logic
        if st.button("Run Validation (Save Copy)"):
            output_path = save_output(df, output_folder, uploaded_file.name)
            st.success(f"✅ Validation complete for {selected_provider} ({selected_year}-{selected_month:02d}).")
            st.info(f"📄 File saved at:\n{output_path}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("Please upload a file and specify an output folder to begin.")
