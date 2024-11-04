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

# Define a function to create the nomogram plot
# This function is cached to avoid re-creating the plot unnecessarily
@st.cache(allow_output_mutation=True)
def plot_nomogram(concentration, time_from_ingestion):
    # Create a figure and axis to plot on
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define a range of time values from 4 to 20 hours
    time_vals = np.linspace(4, 20, 100)

    # Calculate the y-values (concentration levels) for each threshold line based on time
    line_600 = 600 + slope_600 * (time_vals - 4)
    line_450 = 450 + slope_450 * (time_vals - 4)
    line_300 = 300 + slope_300 * (time_vals - 4)
    line_150 = 150 + slope_150 * (time_vals - 4)

    # Plot each threshold line with unique colors and labels
    ax.plot(time_vals, line_600, color="brown", linestyle="--", linewidth=1.5, label="600 mcg/mL Threshold")
    ax.plot(time_vals, line_450, color="purple", linestyle="--", linewidth=1.5, label="450 mcg/mL Threshold")
    ax.plot(time_vals, line_300, color="orange", linestyle="--", linewidth=1.5, label="300 mcg/mL Threshold")
    ax.plot(time_vals, line_150, color="red", linestyle="--", linewidth=1.5, label="150 mcg/mL Threshold")

    # Add labels at specific time points (8, 12, 16, and 20 hours) for each line
    # This makes it easy to see the concentration levels at key times
    for hour in [8, 12, 16, 20]:
        y_600 = 600 + slope_600 * (hour - 4)
        y_450 = 450 + slope_450 * (hour - 4)
        y_300 = 300 + slope_300 * (hour - 4)
        y_150 = 150 + slope_150 * (hour - 4)

        # Position labels slightly offset at the 20-hour mark to prevent overlap
        if hour == 20:
            ax.text(hour, y_600 + 10, f"{y_600:.1f}", color="brown", fontsize=9, ha='center')
            ax.text(hour, y_450 + 5, f"{y_450:.1f}", color="purple", fontsize=9, ha='center')
            ax.text(hour, y_300, f"{y_300:.1f}", color="orange", fontsize=9, ha='center')
            ax.text(hour, y_150 - 5, f"{y_150:.1f}", color="red", fontsize=9, ha='center')
        else:
            ax.text(hour, y_600, f"{y_600:.1f}", color="brown", fontsize=9, ha='center')
            ax.text(hour, y_450, f"{y_450:.1f}", color="purple", fontsize=9, ha='center')
            ax.text(hour, y_300, f"{y_300:.1f}", color="orange", fontsize=9, ha='center')
            ax.text(hour, y_150, f"{y_150:.1f}", color="red", fontsize=9, ha='center')

    # Plot the patient data point (input concentration and time) as a black dot
    ax.scatter(time_from_ingestion, concentration, color="black", s=50, zorder=5)
    ax.text(time_from_ingestion, concentration + 10, f"{concentration} mcg/mL", color="black", fontsize=10, ha='center')

    # Set custom y-axis tick marks for a clearer view, starting from 0
    y_ticks = [0, 100, 150, 225, 300, 375, 450, 525, 600, 700]
    y_labels = ["0", "100", "150", "225", "300", "375", "450", "525", "600", "700"]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)

    # Set x-axis limits from 4 to 20 hours with ticks at every 2 hours
    ax.set_xlim(4, 20)
    ax.set_xticks(np.arange(4, 21, 2))

    # Add plot title, labels, grid, and legend
    ax.set_xlabel("Time from Ingestion (hours)", fontsize=12)
    ax.set_ylabel("Acetaminophen Concentration (mcg/mL)", fontsize=12)
    ax.set_title("Acetaminophen Nomogram", fontsize=14, weight='bold')
    ax.grid(True, linestyle=':', linewidth=0.5)
    ax.legend(loc="upper right", fontsize=10)

    return fig

# Function to calculate the equivalent concentration at 4 hours
def calculate_equivalent_4hr_concentration(concentration, time_from_ingestion):
    result = concentration * (2 ** ((time_from_ingestion - 4) / 4)) if time_from_ingestion >= 4 else "Invalid time"
    return round(result, 1) if isinstance(result, float) else result

# Function to estimate toxicity time based on current concentration
def calculate_toxicity_time(concentration):
    result = 32.9155 - 13.2878 * math.log10(concentration) if concentration > 0 else "Invalid concentration"
    return round(result, 1) if isinstance(result, float) else result

# Function to determine the risk level based on equivalent concentration
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

# Function to provide a recommendation for NAC treatment based on risk level and time
def nac_treatment_recommendation(nomogram_zone, time_from_ingestion):
    if nomogram_zone in ["High Risk Line", "Very High Risk Line", "Critical Zone"] or (
        nomogram_zone == "Possible Risk Line" and time_from_ingestion <= 8):
        return "Yes, NAC treatment indicated"
    else:
        return "No NAC treatment needed"

# Streamlit app structure
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
    fig = plot_nomogram(concentration, time_from_ingestion)
    st.pyplot(fig)
