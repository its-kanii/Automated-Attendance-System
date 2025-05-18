import streamlit as st
import pandas as pd
import os

st.title("📋 Attendance Management System")
st.markdown("View and download daily attendance logs")

log_files = sorted([f for f in os.listdir("attendance") if f.endswith(".csv")])

if not log_files:
    st.warning("No attendance logs found.")
else:
    selected_log = st.selectbox("Select a date", log_files)

    if selected_log:
        df = pd.read_csv(os.path.join("attendance", selected_log))
        st.success(f"Showing records from: {selected_log}")
        st.dataframe(df)

        # Download link
        st.download_button(
            label="📥 Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=selected_log,
            mime='text/csv'
        )