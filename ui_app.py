import streamlit as st
import pandas as pd
from utils.file_loader import load_file, save_output
import datetime
from utils.file_parser import parse_filename, get_financial_month_from_filename


# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Data Quality Checker", layout="centered")

st.title("📊 Data Quality Validation Tool")
st.markdown("Upload your dataset, select parameters, and run validation checks.")

# ========== USER INPUTS ==========

# Provider selection
provider_options = ["RHW", "XYZ", "ABC", "DEF", "GHI"]  # Add more as needed
selected_provider = st.selectbox("🏢 Select Provider", provider_options)

# Financial year selection
current_year = datetime.datetime.now().year
year_options = list(range(2020, current_year + 3))
selected_year = st.selectbox("📅 Select Financial Year", sorted(year_options, reverse=True))

# Financial month selection (April = 1 → March = 12)
financial_months = {
    1: "April",
    2: "May",
    3: "June",
    4: "July",
    5: "August",
    6: "September",
    7: "October",
    8: "November",
    9: "December",
    10: "January",
    11: "February",
    12: "March"
}
selected_fin_month = st.selectbox(
    "🗓️ Select Financial Month (April=1 ... March=12)",
    options=list(financial_months.keys()),
    format_func=lambda x: f"{x} - {financial_months[x]}"
)

# File upload (multi-file allowed)
uploaded_files = st.file_uploader(
    "📁 Upload one or more datasets (Excel or CSV)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

# Output folder
output_folder = st.text_input(
    "📂 Enter output folder path (where the report should be saved)",
    help="Example: C:\\Rajesh\\Personal\\DQ_Output\\RHW\\2025_09"
)

st.markdown("---")

# ========== VALIDATION BUTTON ==========
col1, col2 = st.columns([3, 1])

with col1:
    run_validation = st.button("▶️ Run Validation")

with col2:
    refresh = st.button("🔄 Clear All")

# If refresh button clicked → reset everything
if refresh:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("🔄 Page refreshed successfully. You can start fresh now.")
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# ========== GUIDANCE MESSAGES ==========
if not uploaded_files and not output_folder:
    st.info("📥 Please upload one or more files and specify an output folder path to begin.")
elif uploaded_files and not output_folder:
    st.warning("📂 Please specify an output folder path before running validation.")
elif not uploaded_files and output_folder:
    st.warning("📥 Please upload at least one dataset file to proceed.")
else:
    st.success("✅ Files and output folder ready. Click **Run Validation** to start!")

# ========== PROCESSING ==========
if run_validation:
    if uploaded_files and output_folder:
        st.write(f"### Running validation for Provider: {selected_provider}, FY: {selected_year}, Month: {selected_fin_month} ({financial_months[selected_fin_month]})")

        for uploaded_file in uploaded_files:
            try:
                st.markdown(f"#### 📄 Processing file: `{uploaded_file.name}`")

                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # --- Parse file metadata ---
                    parsed_info = parse_filename(uploaded_file.name)
                    file_month, file_year = get_financial_month_from_filename(uploaded_file.name)

                    # --- Display parsed details ---
                    st.write("📊 **File Metadata Extracted:**")
                    st.json({
                        "Provider Code (from file)": parsed_info.get("provider_code"),
                        "Dataset Type": parsed_info.get("dataset_type"),
                        "File Year (from name)": parsed_info.get("year"),
                        "File Month (from name)": parsed_info.get("month"),
                        "Derived Financial Month": file_month,
                        "Derived Financial Year": file_year
                    })

                    # --- Cross-check against user input ---
                    if parsed_info.get("provider_code") and parsed_info["provider_code"].upper() != selected_provider.upper():
                        st.warning(f"⚠️ Provider mismatch: File has `{parsed_info['provider_code']}`, selected `{selected_provider}`")

                    # --- Load file ---
                    df = load_file(uploaded_file)
                    st.success(f"✅ Loaded '{uploaded_file.name}' successfully.")
                    st.dataframe(df.head(5))

                    # --- Placeholder for validation logic ---
                    output_path = save_output(df, output_folder, uploaded_file.name)

            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {e}")

            else:
                # This runs *only if no error occurred*
                st.success(f"🎯 File `{uploaded_file.name}` processed successfully.")
                st.info(f"📁 Output saved at: {output_path}")


