import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure page
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("📀 Data Sweeper")
st.write("Welcome to the **Data Sweeper ** – your all-in-one solution for data transformation! 🚀")
st.markdown("""
### 🌟 Features:
- **Convert CSV & Excel** files seamlessly.
- **Clean Your Data**: Remove duplicates, fill missing values, and eliminate outliers.
- **Visualize Data**: Interactive charts for quick insights.
- **Download Processed Files** in your desired format.

📌 *Upload your files and start transforming your data now!*
""")

# Sidebar for file upload
st.sidebar.header("📂 Upload Files")
st.sidebar.write("Upload your dataset and start the transformation process.")
uploaded_files = st.sidebar.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    file_data = {}
    
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.sidebar.error(f"Unsupported file type: {file_ext}")
                continue  # Skip unsupported files
        except Exception as e:
            st.sidebar.error(f"Error reading {file.name}: {e}")
            continue

        file_data[file.name] = df

    # Tabs for better organization
    tabs = st.tabs([f"📄 {file}" for file in file_data.keys()])
    
    for idx, (file_name, df) in enumerate(file_data.items()):
        with tabs[idx]:
            st.subheader(f"📊 File Overview: {file_name}")
            st.write(f"**Size:** {len(df)} rows × {len(df.columns)} columns")
            st.write("✔ Preview of your dataset:")
            st.dataframe(df.head())
            
            # Data Cleaning
            st.subheader("🛠 Data Cleaning")
            st.write("Select cleaning options to enhance data quality before transformation.")
            
            col1, col2, col3 = st.columns(3)
            
            if col1.button(f"🗑 Remove Duplicates ({file_name})"):
                df.drop_duplicates(inplace=True)
                st.success("✔ Duplicates removed successfully!")
            
            if col2.button(f"📥 Fill Missing Values ({file_name})"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✔ Missing values filled!")
            
            if col3.button(f"📉 Remove Outliers ({file_name})"):
                for col in df.select_dtypes(include=['number']).columns:
                    q1, q3 = df[col].quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                st.success("✔ Outliers removed!")
            
            # Column Selection
            st.subheader("🎯 Select Columns")
            st.write("Pick the specific columns you need in your transformed dataset.")
            selected_columns = st.multiselect(f"Choose columns to keep ({file_name})", df.columns, default=df.columns)
            df = df[selected_columns]
            
            # Visualization
            st.subheader("📊 Data Visualization")
            st.write("Gain insights into your data with interactive charts.")
            if st.checkbox(f"Show Chart ({file_name})"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
            
            # File Conversion
            st.subheader("⚙ Conversion Options")
            st.write("Select your preferred format and download the processed data.")
            conversion_type = st.radio(f"Convert {file_name} to:", ["CSV", "Excel"], key=file_name)
            
            if st.button(f"🔄 Convert {file_name}"):
                buffer = BytesIO()
                new_ext = ".csv" if conversion_type == "CSV" else ".xlsx"
                new_file_name = file_name.replace(file_ext, new_ext)
                mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False)
                
                buffer.seek(0)
                
                st.download_button(
                    label=f"⬇ Download {new_file_name}",
                    data=buffer,
                    file_name=new_file_name,
                    mime=mime_type
                )
                
                st.success(f"🎉 {file_name} converted to {conversion_type}!")

st.sidebar.markdown("---")
st.sidebar.write("**Developed with ❤️ for data enthusiasts.**")
