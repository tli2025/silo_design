import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from app_utils import create_line_func

st.set_page_config(
    page_title="User Inputs",
    page_icon="📥",
    layout="wide"
)

# --- Define constants and save file path ---
SAVE_FILE = "last_inputs.json"
A_SHEAR_CELL = 0.007146  # m^2 (This is now a global constant)

st.title("📥 Step 1: Enter Your Test Data")
st.markdown("Enter all your measured bulk solid properties and design choices here. All units are SI (kPa, m, kg/m³). When finished, click 'Submit Data'.")
st.markdown("---")

# --- Function to select and display the correct chart ---
def get_design_chart(phi_e, shape):
    """
    Selects the correct chart filename based on user input.
    Returns the filename and a caption.
    """
    # Round phi_e to the nearest 5 degrees to match the charts
    phi_e_rounded = int(5 * round(phi_e / 5))
    
    if shape == "Conical":
        phi_e_clamped = np.clip(phi_e_rounded, 25, 60)
        if phi_e_clamped != phi_e_rounded:
            st.warning(f"$\phi_e$ of {phi_e:.1f}° is outside the chart range [25°, 60°]. Using chart for {phi_e_clamped}°.")
        
        chart_map = {
            25: "fig_10_30.png", 30: "fig_10_31.png", 35: "fig_10_32.png",
            40: "fig_10_33.png", 45: "fig_10_34.png", 50: "fig_10_35.png",
            55: "fig_10_36.png", 60: "fig_10_37.png"
        }
        filename = chart_map.get(phi_e_clamped, "fig_10_33.png") # Default to 40
        caption = f"Fig. {filename.split('_')[1].split('.')[0]}: Mass flow chart for CONICAL hopper with $\phi_e = {phi_e_clamped}^\circ$."
        return filename, caption

    elif shape == "Plane-Flow (Slot)":
        phi_e_clamped = np.clip(phi_e_rounded, 25, 60)
        if phi_e_clamped != phi_e_rounded:
            st.warning(f"$\phi_e$ of {phi_e:.1f}° is outside the chart range [25°, 60°]. Using chart for {phi_e_clamped}°.")

        chart_map = {
            25: "fig_10_38.png", 30: "fig_10_39.png", 35: "fig_10_40.png",
            40: "fig_10_41.png", 45: "fig_10_42.png", 50: "fig_10_43.png",
            55: "fig_10_44.png", 60: "fig_10_45.png"
        }
        filename = chart_map.get(phi_e_clamped, "fig_10_41.png") # Default to 40
        caption = f"Fig. {filename.split('_')[1].split('.')[0]}: Mass flow chart for PLANE-FLOW hopper with $\phi_e = {phi_e_clamped}^\circ$."
        return filename, caption
    
    return None, None

# --- Save and Load Functions ---
def load_inputs():
    """Reads the JSON save file and populates st.session_state."""
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            # Update session_state for each saved key
            for key, value in data.items():
                if key in st.session_state:
                    # Special handling for data_editor data (list of dicts)
                    if key.endswith("_data"):
                         st.session_state[key] = pd.DataFrame(value)
                    else:
                         st.session_state[key] = value
        st.success("Loaded last saved inputs!")
    except FileNotFoundError:
        st.error(f"No save file found ('{SAVE_FILE}'). Using default values.")
    except Exception as e:
        st.error(f"Error loading inputs: {e}")

def save_inputs(data_dict):
    """Saves the provided dictionary to the JSON save file."""
    try:
        # Convert dataframes to list of dicts for JSON serialization
        serializable_data = {}
        for key, value in data_dict.items():
            if isinstance(value, pd.DataFrame):
                serializable_data[key] = value.to_dict('records')
            else:
                serializable_data[key] = value
                
        with open(SAVE_FILE, 'w') as f:
            json.dump(serializable_data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving inputs to '{SAVE_FILE}': {e}")


# Use two columns for a cleaner layout
col1, col2 = st.columns(2)

# --- Define default values in one place (SI UNITS) ---
defaults = {
    "solid_name": "Iron Concentrate",
    "wall_material": "Stainless Steel 304",
    "gamma": 2400.0, # kg/m^3
    "delta": 50.0,
    "wyl_input_method": "Define by N test points",
    "wyl_data": pd.DataFrame([ # Wall Yield Locus
        {"Normal Stress (kPa)": 3.1, "Shear Stress (kPa)": 1.4},
        {"Normal Stress (kPa)": 12.4, "Shear Stress (kPa)": 4.9},
    ]),
    "mu": 0.4, "tau_ad": 0.2, # Adhesion in kPa
    "ff_input_method": "Define by N test points",
    "ff_inst_data": pd.DataFrame([
        {"Consol. Stress σ₁ (kPa)": 3.1, "Strength σc (kPa)": 0.6},
        {"Consol. Stress σ₁ (kPa)": 18.9, "Strength σc (kPa)": 2.5},
    ]),
    "ff_time_data": pd.DataFrame([
        {"Consol. Stress σ₁ (kPa)": 3.1, "Strength σc (kPa)": 1.5},
        {"Consol. Stress σ₁ (kPa)": 18.9, "Strength σc (kPa)": 5.0},
    ]),
    "m_inst": 0.12, "c_inst": 0.2, # Intercept in kPa
    "m_time": 0.22, "c_time": 0.8, # Intercept in kPa
    "flow_pattern": "Mass-Flow",
    "hopper_shape": "Conical",
    "h_f": 6.0,   # m
    "D_silo": 3.0, # m
    "K_janssen": 0.4,
    "theta_prime_manual": 18.0,
    "ff_manual": 1.3,
    "phi_prime_calc": 22.0 # Default calculated value
}

# Initialize session_state keys if they don't exist
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Column 1 Inputs ---
with col1:
    st.subheader("Project Information")
    st.text_input("Solid Name", key="solid_name")
    st.text_input("Wall Material", key="wall_material")

    st.subheader("Solid Properties")
    st.number_input("Bulk Density ($\\rho_b$) [kg/m³]", format="%.2f", key="gamma")
    st.number_input("Effective Angle of Internal Friction ($\\phi_e$) [°]", min_value=0.0, max_value=90.0, format="%.1f", key="delta")
    st.caption(f"Assuming standard shear cell area A = {A_SHEAR_CELL:.6f} m².") # Use global constant

    st.subheader("Wall Yield Locus (WYL)")
    st.radio(
        "WYL Input Method",
        ["Define by N test points", "Define by equation ($\\tau_w = \mu \cdot \\sigma_w + \\tau_{ad}$)"],
        key="wyl_input_method",
        horizontal=True
    )

    phi_prime_calc = 0.0
    wyl_plot_max = 20.0 # Default plot max
    m_wyl, c_wyl = 0.0, 0.0 # Initialize WYL parameters
    wyl_x, wyl_y = [], []
    
    if st.session_state.wyl_input_method == "Define by N test points":
        st.markdown("Enter your test points (Normal Stress vs. Shear Stress) in **kPa**.")
        st.session_state.wyl_data = st.data_editor(
            st.session_state.wyl_data,
            num_rows="dynamic",
            key="wyl_data_editor"
        )
        
        try:
            wyl_points = st.session_state.wyl_data.to_dict('records')
            wyl_x = [p.get("Normal Stress (kPa)") for p in wyl_points if p.get("Normal Stress (kPa)") is not None]
            wyl_y = [p.get("Shear Stress (kPa)") for p in wyl_points if p.get("Shear Stress (kPa)") is not None]
            
            phi_x_angles = []
            if wyl_x and wyl_y and len(wyl_x) >= 2 and len(wyl_x) == len(wyl_y):
                for sigma_w, tau_w in zip(wyl_x, wyl_y):
                    if sigma_w > 1e-6:
                        phi_x_angles.append(np.degrees(np.arctan(tau_w / sigma_w)))
            
            if phi_x_angles:
                phi_prime_calc = np.mean(phi_x_angles)
                st.info(f"Calculated average Wall Friction Angle ($\\phi_x$): **{phi_prime_calc:.1f}°** (from {len(phi_x_angles)} points)")
                wyl_plot_max = max(wyl_x) * 1.5
                _, (m_wyl, c_wyl) = create_line_func(wyl_x, wyl_y) # Get fit params
            else:
                st.warning("Please enter at least 2 WYL data points.")
                
        except Exception as e:
            st.error(f"Error processing WYL data: {e}")
            phi_prime_calc = 0.0

    else: # Define by equation
        st.markdown("Enter the parameters for $\\tau_w = \mu \cdot \\sigma_w + \\tau_{ad}$ (stresses in **kPa**)")
        cols_wyl_eq = st.columns(2)
        cols_wyl_eq[0].number_input("Friction Coeff ($\\mu$)", format="%.3f", key="mu")
        cols_wyl_eq[1].number_input("Adhesion ($\\tau_{ad}$) [kPa]", format="%.3f", key="tau_ad")
        
        m_wyl, c_wyl = st.session_state.mu, st.session_state.tau_ad
        sigma_w_rep = 10.0 # Representative stress of 10 kPa
        tau_w_rep = m_wyl * sigma_w_rep + c_wyl
        if sigma_w_rep > 1e-6:
            phi_prime_calc = np.degrees(np.arctan(tau_w_rep / sigma_w_rep))
            st.info(f"Calculated representative Wall Friction Angle ($\\phi_x$): **{phi_prime_calc:.1f}°** (at $\\sigma_w = 10$ kPa)")
        else:
            phi_prime_calc = 0.0
        wyl_plot_max = 20.0 # Default plot max
    
    # --- WYL Verification Plot ---
    st.markdown("##### WYL Verification Plot")
    try:
        fig_wyl, ax_wyl = plt.subplots()
        sigma_w_plot = np.linspace(0, wyl_plot_max, 50)
        
        if st.session_state.wyl_input_method == "Define by N test points":
            wyl_func, (m_wyl_fit, c_wyl_fit) = create_line_func(wyl_x, wyl_y)
            ax_wyl.plot(sigma_w_plot, wyl_func(sigma_w_plot), 'r--', label=f'Fit: $\\tau_w = {m_wyl_fit:.3f}\\sigma_w + {c_wyl_fit:.3f}$')
            ax_wyl.plot(wyl_x, wyl_y, 'bo', label='Data Points')
        else:
            wyl_func = lambda sigma_w: m_wyl * sigma_w + c_wyl
            ax_wyl.plot(sigma_w_plot, wyl_func(sigma_w_plot), 'r-', label=f'Eq: $\\tau_w = {m_wyl:.3f}\\sigma_w + {c_wyl:.3f}$')

        ax_wyl.set_xlabel("Normal Stress ($\\sigma_w$) [kPa]")
        ax_wyl.set_ylabel("Shear Stress ($\\tau_w$) [kPa]")
        ax_wyl.legend()
        ax_wyl.grid(True)
        ax_wyl.set_ylim(bottom=0)
        ax_wyl.set_xlim(left=0)
        st.pyplot(fig_wyl)
    except Exception as e:
        st.warning(f"Could not draw WYL plot. Error: {e}")

# --- Column 2 Inputs ---
with col2:
    st.subheader("Flow Functions ($\\sigma_c$ vs. $\\sigma_1$)")
    st.markdown("This defines the solid's cohesive strength. The **Time Function (t>0)** is used for the final design.")
    
    st.radio(
        "Flow Function Input Method",
        ["Define by N test points", "Define by equation ($\\sigma_c = m \cdot \\sigma_1 + c$)"],
        key="ff_input_method",
        horizontal=True
    )
    
    sigma_1_plot_max_base = 30.0 # default

    if st.session_state.ff_input_method == "Define by N test points":
        st.markdown("**Instantaneous (t=0)**: Enter test points in **kPa**.")
        st.session_state.ff_inst_data = st.data_editor(
            st.session_state.ff_inst_data,
            num_rows="dynamic",
            key="ff_inst_data_editor"
        )
        
        st.markdown("**Time (t>0)**: Enter test points in **kPa**.")
        st.session_state.ff_time_data = st.data_editor(
            st.session_state.ff_time_data,
            num_rows="dynamic",
            key="ff_time_data_editor"
        )
        
        # --- Verification Plot (from N points) ---
        st.markdown("##### Flow Function Verification Plot")
        try:
            fig, ax = plt.subplots()
            
            inst_data = st.session_state.ff_inst_data.to_dict('records')
            inst_x = [p.get("Consol. Stress σ₁ (kPa)") for p in inst_data if p.get("Consol. Stress σ₁ (kPa)") is not None]
            inst_y = [p.get("Strength σc (kPa)") for p in inst_data if p.get("Strength σc (kPa)") is not None]

            time_data = st.session_state.ff_time_data.to_dict('records')
            time_x = [p.get("Consol. Stress σ₁ (kPa)") for p in time_data if p.get("Consol. Stress σ₁ (kPa)") is not None]
            time_y = [p.get("Strength σc (kPa)") for p in time_data if p.get("Strength σc (kPa)") is not None]
            
            sigma_1_plot_max_base = max(max(inst_x) if inst_x else 0, max(time_x) if time_x else 30)
            if sigma_1_plot_max_base == 0: sigma_1_plot_max_base = 30
            
            sigma_1_plot = np.linspace(0, sigma_1_plot_max_base * 1.5, 50)
            
            if len(inst_x) >= 2:
                ff_inst_func, _ = create_line_func(inst_x, inst_y)
                ax.plot(sigma_1_plot, ff_inst_func(sigma_1_plot), label="Instantaneous FF (t=0)")
                ax.plot(inst_x, inst_y, 'bo', label='Inst. data points')
            
            if len(time_x) >= 2:
                ff_time_func, _ = create_line_func(time_x, time_y)
                ax.plot(sigma_1_plot, ff_time_func(sigma_1_plot), label="Time FF (t>0) (Design)", linestyle='--', color='red')
                ax.plot(time_x, time_y, 'rs', label='Time data points')

            ax.set_xlabel("Consolidation Stress ($\\sigma_1$) [kPa]")
            ax.set_ylabel("Unconfined Yield Strength ($\\sigma_c$) [kPa]")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)
            st.pyplot(fig)
            
        except Exception as e:
            st.warning(f"Could not draw plot. Please enter at least 2 points for each function. Error: {e}")
    
    else: # Define by equation
        st.markdown("**Instantaneous (t=0)**: $\\sigma_c = m \\cdot \\sigma_1 + c$ (stresses in **kPa**)")
        cols_ff_inst_eq = st.columns(2)
        cols_ff_inst_eq[0].number_input("Slope (m)", format="%.4f", key="m_inst")
        cols_ff_inst_eq[1].number_input("Intercept (c) [kPa]", format="%.2f", key="c_inst")
        
        st.markdown("**Time (t>0)**: $\\sigma_c = m \\cdot \\sigma_1 + c$ (stresses in **kPa**)")
        cols_ff_time_eq = st.columns(2)
        cols_ff_time_eq[0].number_input("Slope (m)", format="%.4f", key="m_time")
        cols_ff_time_eq[1].number_input("Intercept (c) [kPa]", format="%.2f", key="c_time")

        # --- Verification Plot (from equation) ---
        st.markdown("##### Flow Function Verification Plot")
        try:
            fig, ax = plt.subplots()
            sigma_1_plot_max_base = 30.0 # default kPa
            if st.session_state.m_time > 0.01:
                sigma_1_plot_max_base = max(30, (st.session_state.c_time * 5) / st.session_state.m_time)
            
            sigma_1_plot = np.linspace(0, sigma_1_plot_max_base, 50)
            
            ff_inst_func = lambda sigma_1: st.session_state.m_inst * sigma_1 + st.session_state.c_inst
            ff_time_func = lambda sigma_1: st.session_state.m_time * sigma_1 + st.session_state.c_time

            ax.plot(sigma_1_plot, ff_inst_func(sigma_1_plot), label="Instantaneous FF (t=0)")
            ax.plot(sigma_1_plot, ff_time_func(sigma_1_plot), label="Time FF (t>0) (Design)", linestyle='--', color='red')

            ax.set_xlabel("Consolidation Stress ($\\sigma_1$) [kPa]")
            ax.set_ylabel("Unconfined Yield Strength ($\\sigma_c$) [kPa]")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not draw plot. Error: {e}")

    st.subheader("Design Choices")
    st.radio("Flow Pattern", ["Mass-Flow", "Funnel-Flow"], key="flow_pattern")
    st.radio("Hopper Shape", ["Conical", "Plane-Flow (Slot)"], key="hopper_shape")

# --- Conditional Inputs (based on selections above) ---
if st.session_state.flow_pattern == "Mass-Flow":
    st.markdown("---")
    st.subheader("Mass-Flow Chart Lookup")
    st.warning(f"Your design requires the chart for **{st.session_state.hopper_shape}** and **$\\phi_e \\approx {st.session_state.delta:.1f}^\circ$**.")
    
    chart_file, chart_caption = get_design_chart(st.session_state.delta, st.session_state.hopper_shape)
    
    if chart_file:
        st.image(f"assets/{chart_file}", caption=chart_caption)
        st.markdown(f"**Instructions:**")
        st.markdown(f"1.  Find your **Wall Friction Angle ($\\phi_x = {phi_prime_calc:.1f}^\circ$)** on the y-axis.")
        st.markdown(f"2.  Move right to the **Mass Flow Boundary** (heavy dashed line).")
        st.markdown(f"3.  Read the corresponding **Hopper Angle ($\\Theta_c$ or $\\Theta_p$)** on the x-axis. Subtract a safety margin (e.g., 3°) and enter it below.")
        st.markdown(f"4.  At that design point (your $\\Theta$, your $\\phi_x$), find the **Flow Factor ($ff$)** by interpolating between the solid contour lines.")

        lookup_cols = st.columns(2)
        lookup_cols[0].number_input("Enter Design Hopper Angle ($\\Theta$) [°]", format="%.1f", key="theta_prime_manual")
        lookup_cols[1].number_input("Enter Flow Factor ($ff$) from chart", format="%.2f", key="ff_manual")
    
    else:
        st.error("Could not find a matching design chart for the selected parameters.")

elif st.session_state.flow_pattern == "Funnel-Flow":
    with col2:
        st.markdown("#### Funnel-Flow Silo Dimensions")
        st.markdown("Please provide the silo dimensions for the 'Upper Bound' (Janssen) ratholing calculation.")
        st.number_input("Filling Height (h_f) [m]", format="%.1f", key="h_f")
        st.number_input("Silo Diameter/Width (D) [m]", format="%.1f", key="D_silo")
        st.number_input("Janssen Stress Ratio (K)", format="%.2f", help="Typically 0.4-0.5", key="K_janssen")

st.markdown("---")

# --- Load Button ---
st.button("Load Last Inputs", on_click=load_inputs)

# --- Submit Button ---
if st.button("Submit Data and Go to Results", type="primary"):
    
    # Store the DataFrame data as a list of dicts for JSON serialization
    inputs_to_save = {
        "solid_name": st.session_state.solid_name,
        "wall_material": st.session_state.wall_material,
        "gamma": st.session_state.gamma,
        "delta": st.session_state.delta,
        "phi_prime_calc": phi_prime_calc, 
        
        "wyl_input_method": st.session_state.wyl_input_method,
        "wyl_data": st.session_state.wyl_data.to_dict('records'),
        "mu": st.session_state.mu,
        "tau_ad": st.session_state.tau_ad,
        "m_wyl": m_wyl, # Save the calculated fit
        "c_wyl": c_wyl, # Save the calculated fit
        
        "ff_input_method": st.session_state.ff_input_method,
        "ff_inst_data": st.session_state.ff_inst_data.to_dict('records'),
        "ff_time_data": st.session_state.ff_time_data.to_dict('records'),
        
        "m_inst": st.session_state.m_inst, "c_inst": st.session_state.c_inst, 
        "m_time": st.session_state.m_time, "c_time": st.session_state.c_time, 

        "flow_pattern": st.session_state.flow_pattern,
        "hopper_shape": st.session_state.hopper_shape,
        "h_f": st.session_state.h_f,
        "D_silo": st.session_state.D_silo,
        "K_janssen": st.session_state.K_janssen,
        "theta_prime_manual": st.session_state.theta_prime_manual, 
        "ff_manual": st.session_state.ff_manual,
        "A_shear_cell": A_SHEAR_CELL
    }
    
    # Save this dictionary to the session_state for the results page
    st.session_state.inputs = inputs_to_save
    
    # Save to file
    save_inputs(inputs_to_save)
    
    st.success("Data saved! Please navigate to the '4_Results' page in the sidebar.")
    st.page_link("pages/4_Results.py", label="**Go to Results Page →**")