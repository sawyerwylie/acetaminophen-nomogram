# app.py

# Import necessary libraries
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Define constants for the slopes of each threshold line
# These are calculated based on specific y-values at 4 and 20 hours
slope_600 = (37.5 - 600) / (20 - 4)  # Slope for the 600 mcg/mL line
slope_450 = (28.125 - 450) / (20 - 4)  # Slope for the 450 mcg/mL line
slope_300 = (18.75 - 300) / (20 - 4)  # Slope for the 300 mcg/mL line
slope_150 = (9.375 - 150) / (20 - 4)  # Slope for the 150 mcg/mL line

# Define a function to create the nomogram plot with consistent, straight, balanced lines
def plot_nomogram_reverted_parallel_lines(concentration, time_from_ingestion):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Using consistent, straight slopes to ensure visual balance
    line_150_refined = np.linspace(150, 9.375, len(hours))  # Consistent slope for straightness
    line_300_refined = np.linspace(300, 18.75, len(hours))
    line_450_refined = np.linspace(450, 28.125, len(hours))
    line_600_refined = np.linspace(600, 37.5, len(hours))

    # Plot each line using the consistent, visually straight slopes
    ax.plot(hours, line_150_refined, color="red", linestyle="--", linewidth=1.5, label="150 mcg/mL Threshold")
    ax.plot(hours, line_300_refined, color="orange", linestyle="--", linewidth=1.5, label="300 mcg/mL Threshold")
    ax.plot(hours, line_450_refined, color="purple", linestyle="--", linewidth=1.5, label="450 mcg/mL Threshold")
    ax.plot(hours, line_600_refined, color="brown", linestyle="--", linewidth=1.5, label="600 mcg/mL Threshold")

    # Plot the patient's concentration and ingestion time as a data point
    ax.scatter(time_from_ingestion, concentration, color="black", s=50, zorder=5)
    ax.text(time_from_ingestion, concentration + 10, f"{concentration} mcg/mL", color="black", fontsize=10, ha='center')

    # Y-axis tick positions for accurate and visually aligned values
    custom_y_ticks = [0, 100, 150, 225, 300, 375, 450, 525, 600, 700]
    custom_y_labels = ["0", "100", "150", "225", "300", "375", "450", "525", "600", "700"]
    ax.set_yticks(custom_y_ticks)
    ax.set_yticklabels(custom_y_labels)

    # Set x-axis limits and ticks as before
    ax.set_xlim(4, 20)
    ax.set_xticks(np.arange(4, 21, 2))

    # Add title, labels, grid, and legend
    ax.set_xlabel("Time from Ingestion (hours)", fontsize=12)
    ax.set_ylabel("Acetaminophen Concentration (mcg/mL)", fontsize=12)
    ax.set_title("Acetaminophen Nomogram with Balanced Lines", fontsize=14, weight='bold')
    ax.grid(True, linestyle=':', linewidth=0.5)
    ax.legend(loc="upper right", fontsize=10)

    return fig

# Supporting calculations with rounding and terminology matching Google Sheet
def calculate_equivalent_4hr_concentration(concentration, time_from_ingestion):
    result = concentration * (2 ** ((time_from_ingestion - 4) / 4)) if time_from_ingestion >= 4 else "Invalid time"
    return round(result, 1) if isinstance(result, float) else result

def calculate_toxicity_time(concentration):
    result = 32.9155 - 13.2878 * math.log10(concentration) if concentration > 0 else "Invalid concentration"
    return round(result, 1) if isinstance(result, float) else result

def determine_nomogram_zone(equiv_conc):
    if equiv_conc < 150:
        return "Below Treatment Line"
    elif 150 <= equiv_conc < 300:
        return "Possible Risk Line"
    elif 300 <= equiv_conc < 450:
        return "High Risk Line"
    elif 450 <= equiv_conc < 600:
        return "Very High Risk Line"
    else:
        return "Critical Zone"

# Simplified NAC Recommendation
def nac_treatment_recommendation(nomogram_zone, time_from_ingestion):
    if nomogram_zone in ["High Risk Line", "Very High Risk Line", "Critical Zone"] or (
        nomogram_zone == "Possible Risk Line" and time_from_ingestion <= 8):
        return "Yes, NAC treatment indicated"
    else:
        return "No NAC treatment needed"

# Streamlit App
st.title("Acetaminophen Nomogram Calculator")

# Input fields for concentration and time from ingestion
concentration = st.number_input("Enter Acetaminophen Concentration (mcg/mL):", min_value=0.0)
time_from_ingestion = st.number_input("Enter Time from Ingestion (hours):", min_value=4.0, max_value=20.0)

# Perform calculations
equiv_concentration_4hr = calculate_equivalent_4hr_concentration(concentration, time_from_ingestion)
toxicity_time = calculate_toxicity_time(concentration)
nomogram_zone = determine_nomogram_zone(equiv_concentration_4hr)
nac_recommendation = nac_treatment_recommendation(nomogram_zone, time_from_ingestion)

# Display the calculated results
st.subheader("Results")
st.write(f"Equivalent Concentration at 4 Hours: {equiv_concentration_4hr}")
st.write(f"Estimated Toxicity Time: {toxicity_time} hours")
st.write(f"Nomogram Zone: {nomogram_zone}")
st.write(f"NAC Treatment Recommendation: {nac_recommendation}")

# Display the nomogram plot if both inputs are provided
if concentration and time_from_ingestion:
    fig = plot_nomogram_reverted_parallel_lines(concentration, time_from_ingestion)
    st.pyplot(fig)
