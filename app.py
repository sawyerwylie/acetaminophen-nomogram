# app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# 1. Input Fields
st.title("Acetaminophen Nomogram Calculator")

# Input for concentration and time
concentration = st.number_input("Enter Acetaminophen Concentration (mcg/mL):", min_value=0.0)
time_from_ingestion = st.number_input("Enter Time from Ingestion (hours):", min_value=0.0)

# 2. Calculations based on Excel formulas

# Equivalent concentration at 4 hours (based on Excel formula)
if concentration == 0 or time_from_ingestion == 0:
    equiv_concentration_4h = "Enter Data"
else:
    equiv_concentration_4h = concentration * (2 ** ((time_from_ingestion - 4) / 4))

# Nomogram Zone Classification
if equiv_concentration_4h == "Enter Data":
    nomogram_zone = "Enter Data"
else:
    if equiv_concentration_4h < 150:
        nomogram_zone = "<150"
    elif 150 <= equiv_concentration_4h < 300:
        nomogram_zone = "150-300"
    elif 300 <= equiv_concentration_4h < 450:
        nomogram_zone = "300-450"
    elif 450 <= equiv_concentration_4h < 600:
        nomogram_zone = "450-600"
    else:
        nomogram_zone = ">600"

# NAC Treatment Recommendation based on Nomogram Zone and Time
if nomogram_zone == "Enter Data":
    nac_treatment = "Enter Data"
else:
    if nomogram_zone == "<150":
        nac_treatment = "No treatment indicated"
    elif nomogram_zone == "150-300":
        nac_treatment = "Yes, routine dosing"
    elif nomogram_zone in ["300-450", "450-600", ">600"] and time_from_ingestion <= 8:
        nac_treatment = "Yes, double dosing"
    else:
        nac_treatment = "Yes, routine dosing"

# Dosing Modification based on NAC Treatment
dosing_modification = "Double dose of 3rd bag to 200 mg/kg (12.5 mg/kg/h)" if nac_treatment == "Yes, double dosing" else "None"

# Toxicologist Recommendation for High Concentrations
toxicologist_recommendation = "Call toxicologist for additional recommendations" if concentration >= 600 else ""

# Time for Toxicity (using Excel's logarithmic relationship)
if concentration == 0:
    time_for_toxicity = "Enter Data"
else:
    toxicity_time_value = 32.9155 - 13.2878 * math.log10(concentration)
    time_for_toxicity = toxicity_time_value if toxicity_time_value > 4 else "-"

# Threshold concentration for treatment (from cell B5 formula)
threshold_concentration = math.exp(5.298317 - (time_from_ingestion - 4) * 0.1732868) * 0.75

# 3. Display Calculations
st.subheader("Results")
st.write(f"Equivalent Concentration at 4 Hours: {equiv_concentration_4h}")
st.write(f"Nomogram Zone: {nomogram_zone}")
st.write(f"NAC Treatment: {nac_treatment}")
st.write(f"Dosing Modification: {dosing_modification}")
st.write(f"Toxicologist Recommendation: {toxicologist_recommendation}")
st.write(f"Time (hours) for Toxicity: {time_for_toxicity}")
st.write(f"Threshold [APAP] (mcg/mL) for Treatment: {threshold_concentration:.2f}")

# 4. Nomogram Plot
fig, ax = plt.subplots(figsize=(8, 6))

# Set up x-axis and y-axis range with fixed limits
time_vals = np.linspace(0, 24, 100)
threshold_vals = 150 * np.exp(-0.3 * time_vals)

# Plot the treatment threshold line
ax.plot(time_vals, threshold_vals, label="Treatment Threshold", color="red", linestyle="--")

# Plot the patient's data point
ax.scatter(time_from_ingestion, concentration, color="blue", label="Patient Data Point", zorder=5)

# Set axis limits and labels for clarity
ax.set_xlim(0, 24)
ax.set_ylim(0, 300)
ax.set_xlabel("Time from Ingestion (hours)", fontsize=12)
ax.set_ylabel("Acetaminophen Concentration (mcg/mL)", fontsize=12)

# Title and legend
ax.set_title("Acetaminophen Nomogram", fontsize=14, weight='bold')
ax.legend(loc="upper right")
ax.grid(True)

st.pyplot(fig)
