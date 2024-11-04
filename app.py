# app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Constants for slopes and starting y-values based on given specifications
slope_600 = (37.5 - 600) / (20 - 4)  # Slope for the 600 mcg/mL line
slope_450 = (28.125 - 450) / (20 - 4)  # Slope for the 450 mcg/mL line
slope_300 = (18.75 - 300) / (20 - 4)  # Slope for the 300 mcg/mL line
slope_150 = (9.375 - 150) / (20 - 4)  # Slope for the 150 mcg/mL line

# Function to create the nomogram plot
def plot_nomogram(concentration, time_from_ingestion):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define time values from 4 to 20 hours
    time_vals = np.linspace(4, 20, 100)

    # Define the threshold lines
    line_600 = 600 + slope_600 * (time_vals - 4)
    line_450 = 450 + slope_450 * (time_vals - 4)
    line_300 = 300 + slope_300 * (time_vals - 4)
    line_150 = 150 + slope_150 * (time_vals - 4)

    # Plot each threshold line with colors and labels
    ax.plot(time_vals, line_600, color="brown", linestyle="--", linewidth=1.5, label="600 mcg/mL Threshold")
    ax.plot(time_vals, line_450, color="purple", linestyle="--", linewidth=1.5, label="450 mcg/mL Threshold")
    ax.plot(time_vals, line_300, color="orange", linestyle="--", linewidth=1.5, label="300 mcg/mL Threshold")
    ax.plot(time_vals, line_150, color="red", linestyle="--", linewidth=1.5, label="150 mcg/mL Threshold")

    # Calculate and annotate y-values at 8, 12, 16, and 20 hours with staggered positions at 20 hours
    for hour in [8, 12, 16, 20]:
        y_600 = 600 + slope_600 * (hour - 4)
        y_450 = 450 + slope_450 * (hour - 4)
        y_300 = 300 + slope_300 * (hour - 4)
        y_150 = 150 + slope_150 * (hour - 4)

        # Regular label positions for 8, 12, and 16 hours
        ax.text(hour, y_600, f"{y_600:.1f}", color="brown", fontsize=9, ha='center')
        ax.text(hour, y_450, f"{y_450:.1f}", color="purple", fontsize=9, ha='center')
        ax.text(hour, y_300, f"{y_300:.1f}", color="orange", fontsize=9, ha='center')
        ax.text(hour, y_150, f"{y_150:.1f}", color="red", fontsize=9, ha='center')

        # Staggered positions for the 20-hour mark to avoid overlap
        if hour == 20:
            ax.text(hour, y_600 + 10, f"{y_600:.1f}", color="brown", fontsize=9, ha='center')  # Slightly above
            ax.text(hour, y_450 + 5, f"{y_450:.1f}", color="purple", fontsize=9, ha='center')   # Slightly above
            ax.text(hour, y_300, f"{y_300:.1f}", color="orange", fontsize=9, ha='center')       # Centered
            ax.text(hour, y_150 - 5, f"{y_150:.1f}", color="red", fontsize=9, ha='center')      # Slightly below

    # Plot the patient data point and label it
    ax.scatter(time_from_ingestion, concentration, color="black", s=50, zorder=5)
    ax.text(time_from_ingestion, concentration + 10, f"{concentration} mcg/mL", color="black", fontsize=10, ha='center')

    # Custom y-axis ticks to match non-linear spacing, starting from 0
    y_ticks = [0, 100, 150, 225, 300, 375, 450, 525, 600, 700]
    y_labels = ["0", "100", "150", "225", "300", "375", "450", "525", "600", "700"]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)

    # Set x-axis limits and ticks from 4 to 20 hours
    ax.set_xlim(4, 20)
    ax.set_xticks(np.arange(4, 21, 2))

    # Title, labels, grid, and legend
    ax.set_xlabel("Time from Ingestion (hours)", fontsize=12)
    ax.set_ylabel("Acetaminophen Concentration (mcg/mL)", fontsize=12)
    ax.set_title("Acetaminophen Nomogram", fontsize=14, weight='bold')
    ax.grid(True, linestyle=':', linewidth=0.5)
    ax.legend(loc="upper right", fontsize=10)

    return fig

# Supporting calculations for Equivalent 4-Hour Concentration, Toxicity Time, and NAC Treatment Recommendation
def calculate_equivalent_4hr_concentration(concentration, time_from_ingestion):
    return concentration * (2 ** ((time_from_ingestion - 4) / 4)) if time_from_ingestion >= 4 else "Invalid time"

def calculate_toxicity_time(concentration):
    return 32.9155 - 13.2878 * math.log10(concentration) if concentration > 0 else "Invalid concentration"

def determine_nomogram_zone(equiv_conc):
    if equiv_conc < 150:
        return "Low Risk"
    elif 150 <= equiv_conc < 300:
        return "Moderate Risk"
    elif 300 <= equiv_conc < 450:
        return "High Risk"
    elif 450 <= equiv_conc < 600:
        return "Very High Risk"
    else:
        return "Critical Zone"

def nac_treatment_recommendation(nomogram_zone, time_from_ingestion):
    if nomogram_zone in ["High Risk", "Very High Risk", "Critical Zone"]:
        return "Yes, NAC treatment indicated"
    elif nomogram_zone == "Moderate Risk" and time_from_ingestion <= 8:
        return "Yes, NAC treatment indicated with monitoring"
    else:
        return "No NAC treatment needed"

# Streamlit App
st.title("Acetaminophen Nomogram Calculator")

# Input fields for concentration and time
concentration = st.number_input("Enter Acetaminophen Concentration (mcg/mL):", min_value=0.0)
time_from_ingestion = st.number_input("Enter Time from Ingestion (hours):", min_value=4.0, max_value=20.0)

# Calculate Equivalent 4-Hour Concentration, Toxicity Time, Nomogram Zone, and NAC Treatment Recommendation
equiv_concentration_4hr = calculate_equivalent_4hr_concentration(concentration, time_from_ingestion)
toxicity_time = calculate_toxicity_time(concentration)
nomogram_zone = determine_nomogram_zone(equiv_concentration_4hr)
nac_recommendation = nac_treatment_recommendation(nomogram_zone, time_from_ingestion)

# Display the calculated values
st.subheader("Results")
st.write(f"Equivalent Concentration at 4 Hours: {equiv_concentration_4hr}")
st.write(f"Estimated Toxicity Time: {toxicity_time} hours")
st.write(f"Nomogram Zone: {nomogram_zone}")
st.write(f"NAC Treatment Recommendation: {nac_recommendation}")

# Display the nomogram plot
if concentration and time_from_ingestion:
    fig = plot_nomogram(concentration, time_from_ingestion)
    st.pyplot(fig)
