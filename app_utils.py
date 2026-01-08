import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# --- Ratholing Functions (Funnel Flow) ---

# Digitized data from Schulze, Fig. 10.19 (as provided by user)
f_phi_i_data = {
    "phi_i": [30, 35, 40, 45, 50, 55, 60, 65, 70],
    "f":     [2.39141, 2.94697, 3.55303, 4.28535, 5.05556, 6.09091, 7.56818, 9.46212, 11.6843]
}
f_phi_i_func = interp1d(f_phi_i_data["phi_i"], f_phi_i_data["f"], fill_value="extrapolate")

def get_f_phi_i(phi_lin):
    """
    Interpolates f(phi_i) from digitized data of Schulze, Fig. 10.19.
    We use phi_lin as the input for phi_i.
    """
    st.info("Calculating f($\\phi_i$) using digitized data from Schulze Fig. 10.19.")
    return float(f_phi_i_func(phi_lin))

def get_phi_lin(delta):
    """
    Placeholder. The true phi_lin (angle of linearized yield locus)
    should be derived from test data, but is often close to phi_e (delta).
    We use delta as an approximation.
    """
    st.warning(f"Using Effective Angle of Friction ($\\phi_e$ = {delta:.1f}°) as an approximation for $\\phi_{{lin}}$. A more precise design would use the measured $\\phi_{{lin}}$ vs. $\\sigma_1$ relationship.", icon="⚠️")
    return delta

def get_flow_factor_ffp(phi_e, phi_lin, f_phi_i):
    """
    Calculates the flow factor for ratholing (ffp) using Schulze, Eq. 10.11.
    """
    st.info("Calculating flow factor for ratholing ($ff_p$) using Schulze Eq. 10.11.")
    
    # Convert to radians for numpy functions
    phi_e_rad = np.radians(phi_e)
    
    ff_p = ((1 + np.sin(phi_e_rad)) / (4 * np.sin(phi_e_rad))) * f_phi_i
    
    # Apply constraint from Schulze 10.3.2.3
    if ff_p < 1.7:
        st.warning(f"Calculated $ff_p$ ({ff_p:.2f}) is < 1.7. Using $ff_p = 1.7$ as per Schulze 10.3.2.3.", icon="⚠️")
        return 1.7
    else:
        return ff_p

# --- Other Helpers ---
def create_line_func(x_vals, y_vals):
    """
    Creates a linear function y = mx + c from lists of x and y values.
    Performs a 1st order polynomial fit (linear regression).
    """
    if len(x_vals) < 2 or len(y_vals) < 2:
        # Not enough data to fit a line
        return (lambda x: 0), (0, 0)
        
    x_vals_np = np.array(x_vals, dtype=float)
    y_vals_np = np.array(y_vals, dtype=float)

    if np.all(np.isclose(x_vals_np, x_vals_np[0])):
        # Handle vertical line case, though unlikely for this data
        m, c = 0, np.mean(y_vals_np)
        return (lambda x: np.mean(y_vals_np)), (m, c)
        
    m, c = np.polyfit(x_vals_np, y_vals_np, 1)
    return (lambda x: m * x + c), (m, c)