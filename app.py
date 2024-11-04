# app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Define constants for each line threshold to ensure straight, parallel lines on a semi-logarithmic scale
hours = [4, 8, 12, 16, 20]
line_150_points = [150, 75, 37.5, 18.75, 9.375]
line_300_points = [300, 150, 75, 37.5, 18.75]
line_450_points = [450, 225, 112.5, 56.25, 28.125]
line_600_points = [600, 300, 150, 75, 37.5]

# Cache the plotting function to reduce re-rendering times
@st.cache_resource
def plot_nomogram_final_with_legend(concentration, time_from_ingestion):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot each threshold line
    ax.plot(hours, line_150_points, color="red", linestyle="--", linewidth=1.5, label="150 mcg/mL Threshold")
    ax.plot(hours, line_300_points, color="orange", linestyle="--", linewidth=1.5, label="300 mcg/mL Threshold")
    ax.plot(hours, line_450_points, color="purple", linestyle="--", linewidth=1.5, label="450 mcg/mL Threshold")
    ax.plot(hours, line_600_points, color="brown", linestyle="--", linewidth=1.5, label="600 mcg/mL Threshold")

    # Label each point on the lines with their respective concentration values
    for h, y_150, y_300, y_450, y_600 in zip(hours, line_150_points, line_300_points, line_450_points, line_600_points):
        ax.text(h, y_150, f"{y_150}", color="red", fontsize=8, ha='left', va='center')
        ax.text(h, y_300, f"{y_300}", color="orange", fontsize=8, ha='left', va='center')
        ax.text(h, y_450, f"{y_450}", color="purple", fontsize=8, ha='left', va='center')
        ax.text(h, y_600, f"{y_600}", color="brown", fontsize=8, ha='left', va='center')

    # Plot the patient's concentration and ingestion time as a black "x" data point
    ax.scatter(time_from_ingestion, concentration, color="black", s=50, marker='x', label="Current Patient", zorder=5)
    ax.text(time_from_ingestion, concentration + 10, f"{concentration} mcg/mL", color="black", fontsize=10, ha='center')

    # Set the y-axis to a logarithmic scale
    ax.set_yscale("log")

    # Custom y-axis labels to match concentrations
    custom_y_ticks = [600, 450, 300, 150, 75, 37.5, 18.75, 9.375]
    custom_y_labels = ["600", "450", "300", "150", "75", "37.5", "18.75", "9.375"]
    ax.set_yticks(custom_y_ticks)
    ax.set_yticklabels(custom_y_labels)

    # Set x-axis limits and ticks
    ax.set_xlim(4, 20)
    ax.set_xticks(np.arange(4, 21, 2))

    # Add title, labels, grid, and legend
    ax.set_xlabel("Time from Ingestion (hours)", fontsize=12)
    ax.set_ylabel("Acetaminophen Concentration (mcg/mL)", fontsize=12)
    ax.set_title("Acetaminophen Nomogram", fontsize=14, weight='bold')
    ax.grid(True, linestyle=':', linewidth=0.5)
    ax.legend(loc="upper right", fontsize=10)

    return fig

# Supporting functions for calculations
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

def nac_treatment_recommendation(nomogram_zone, time_from_ingestion):
    if nomogram_zone in ["High Risk Line", "Very High Risk Line", "Critical Zone"] or (
        nomogram_zone == "Possible Risk Line" and time_from_ingestion <= 8):
        return "Yes, NAC treatment indicated"
    else:
        return "No NAC treatment needed"

# Streamlit App Configuration
st.title("Acetaminophen Nomogram Calculator")

# Input fields for acetaminophen concentration and time from ingestion
concentration = st.number_input("Enter Acetaminophen Concentration (mcg/mL):", min_value=0.0)
time_from_ingestion = st.number_input("Enter Time from Ingestion (hours):", min_value=4.0, max_value=20.0)

# Display a button to calculate and render outputs only when clicked
if st.button("Calculate"):
    # Perform calculations for equivalent concentration, toxicity time, and NAC recommendation
    equiv_concentration_4hr = calculate_equivalent_4hr_concentration(concentration, time_from_ingestion)
    toxicity_time = calculate_toxicity_time(concentration)
    nomogram_zone = determine_nomogram_zone(equiv_concentration_4hr)
    nac_recommendation = nac_treatment_recommendation(nomogram_zone, time_from_ingestion)

    # Display the results
    st.subheader("Results")
    st.write(f"Equivalent Concentration at 4 Hours: {equiv_concentration_4hr}")
    st.write(f"Estimated Toxicity Time: {toxicity_time} hours")
    st.write(f"Nomogram Zone: {nomogram_zone}")
    st.write(f"NAC Treatment Recommendation: {nac_recommendation}")

    # Display the final graph with the patient's data point if inputs are provided
    fig = plot_nomogram_final_with_legend(concentration, time_from_ingestion)
    st.pyplot(fig)
