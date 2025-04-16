
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.butterworth_tools import apply_named_bands, summarize_band, export_filtered_csv

st.set_page_config(page_title="Filter Signal", layout="wide")
st.title("🔍 Filter Signal (Butterworth)")

uploaded_file = st.file_uploader("Upload CSV file with time and signal columns", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully.")

    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Choose time and signal columns
    cols = df.columns.tolist()
    time_col = st.selectbox("Select Time Column", cols)
    signal_col = st.selectbox("Select Signal Column", cols)

    if st.button("Apply Butterworth Filters"):
        time_data = df[time_col].values
        signal_data = df[signal_col].values

        with st.spinner("Filtering..."):
            band_signals = apply_named_bands(time_data, signal_data)

        st.write("### Filtered Signal Plots")

        fig, ax = plt.subplots(figsize=(10, 5))
        for label, sig in band_signals.items():
            ax.plot(time_data, sig, label=label)
        ax.set_title("Filtered Components")
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitude")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.write("### Summary Stats")
        for label, sig in band_signals.items():
            stats = summarize_band(sig)
            st.write(f"**{label}**: Max = {stats['max']:.4f}, Min = {stats['min']:.4f}, Std = {stats['std']:.4f}")

        if st.checkbox("Export filtered signals as CSV"):
            export_filtered_csv(time_data, band_signals, prefix="butter")
            st.success("Filtered CSVs saved to working directory.")
