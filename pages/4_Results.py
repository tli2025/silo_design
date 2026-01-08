import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from app_utils import (
    get_f_phi_i,
    get_phi_lin,
    get_flow_factor_ffp,
    create_line_func
)

st.set_page_config(
    page_title="Design Results",
    page_icon="📊",
    layout="wide"
)

# --- Define constants ---
g = 9.81 # m/s^2

st.title("📊 Step 2: Design Results & Plots")

# Check if inputs exist in the session state
if 'inputs' not in st.session_state:
    st.error("No input data found. Please go to the '3_User_Inputs' page and submit your data.")
    st.page_link("pages/3_User_Inputs.py", label="**← Go to Inputs Page**")
else:
    # Load all variables from session_state
    inputs = st.session_state.inputs
    solid_name = inputs["solid_name"]
    wall_material = inputs["wall_material"]
    gamma = inputs["gamma"] # This is rho_b in kg/m^3
    delta = inputs["delta"]
    phi_prime_calc = inputs["phi_prime_calc"] 
    
    # Load Flow Function method and data
    ff_input_method = inputs["ff_input_method"]
    ff_inst_data = inputs["ff_inst_data"] # List of dicts
    ff_time_data = inputs["ff_time_data"] # List of dicts
    m_inst_eq, c_inst_eq = inputs["m_inst"], inputs["c_inst"] # Equation inputs (kPa)
    m_time_eq, c_time_eq = inputs["m_time"], inputs["c_time"] # Equation inputs (kPa)

    # Load WYL fit parameters
    m_wyl = inputs.get("m_wyl", 0.0) 
    c_wyl = inputs.get("c_wyl", 0.0)

    flow_pattern = inputs["flow_pattern"]
    hopper_shape = inputs["hopper_shape"]
    h_f = inputs["h_f"]       # m
    D_silo = inputs["D_silo"] # m
    K_janssen = inputs["K_janssen"]
    
    theta_prime = inputs["theta_prime_manual"]
    ff_value = inputs["ff_manual"]

    # --- Process Inputs into Usable Functions (all stress in kPa) ---
    if ff_input_method == "Define by N test points":
        inst_x = [p.get("Consol. Stress σ₁ (kPa)") for p in ff_inst_data if p.get("Consol. Stress σ₁ (kPa)") is not None]
        inst_y = [p.get("Strength σc (kPa)") for p in ff_inst_data if p.get("Strength σc (kPa)") is not None]
        time_x = [p.get("Consol. Stress σ₁ (kPa)") for p in ff_time_data if p.get("Consol. Stress σ₁ (kPa)") is not None]
        time_y = [p.get("Strength σc (kPa)") for p in ff_time_data if p.get("Strength σc (kPa)") is not None]
        
        ff_inst_func, (m_inst, c_inst) = create_line_func(inst_x, inst_y)
        ff_time_func, (m_time, c_time) = create_line_func(time_x, time_y)
        
        sigma_1_plot_max_base = max(max(inst_x) if inst_x else 0, max(time_x) if time_x else 30)
    else: 
        m_inst, c_inst = m_inst_eq, c_inst_eq
        m_time, c_time = m_time_eq, c_time_eq
        
        ff_inst_func = lambda sigma_1: m_inst * sigma_1 + c_inst
        ff_time_func = lambda sigma_1: m_time * sigma_1 + c_time
        
        sigma_1_plot_max_base = 30 
        if m_time > 0.01:
             sigma_1_plot_max_base = max(30, (c_time * 5) / m_time)


    st.header("Design Results")
    results_cols = st.columns(2)
    
    with results_cols[0]:
        st.subheader("Summary of Your Inputs")
        st.markdown(
            f" - **Solid:** {solid_name} on {wall_material}\n"
            f" - **Bulk Density ($\\rho_b$):** {gamma} kg/m³\n"
            f" - **Effective Angle of Internal Friction ($\\phi_e$):** {delta}°\n"
            f" - **Avg. Wall Friction ($\\phi_x$):** {phi_prime_calc:.1f}°\n"
            f" - **WYL Fit:** '$\\tau_w = {m_wyl:.3f} \cdot \\sigma_w + {c_wyl:.3f}$ (kPa)\n"
            f" - **Instant. FF ($t=0$):** '$\\sigma_c = {m_inst:.3f} \cdot \\sigma_1 + {c_inst:.1f}$ (kPa)\n"
            f" - **Time FF ($t>0$):** '$\\sigma_c = {m_time:.3f} \cdot \\sigma_1 + {c_time:.1f}$ (kPa)"
        )

    # --- Mass-Flow Calculation ---
    if flow_pattern == "Mass-Flow":
        with results_cols[0]:
            st.subheader("Mass-Flow Design (Schulze 10.3.1)")
            
            try:
                st.info(f"Using manual inputs: $\\Theta = {theta_prime:.1f}^\circ$ and $ff = {ff_value:.2f}$")
                
                ff_line_func = lambda sigma_1: sigma_1 / ff_value
                ff_design_func = ff_time_func
                intersection_func = lambda sigma_1: ff_design_func(sigma_1) - ff_line_func(sigma_1)
                
                sigma_1_crit_kpa = fsolve(intersection_func, sigma_1_plot_max_base / 2)[0] 
                sigma_c_crit_kpa = ff_design_func(sigma_1_crit_kpa) 
                
                # --- Convert to Pa for physics equations ---
                sigma_c_crit_pa = sigma_c_crit_kpa * 1000
                
                if hopper_shape == "Conical":
                    B_min = (2 * sigma_c_crit_pa) / (gamma * g) 
                    caption_text = f"Calculated using Schulze Eq. 10.6b: $d_{{crit}} = 2 \\cdot \\sigma_{{c,crit}} / (\\rho_b \\cdot g) = (2 \\cdot {sigma_c_crit_pa:.1f} Pa) / ({gamma} \\cdot {g})$"
                else: # Plane-Flow (Slot)
                    B_min = sigma_c_crit_pa / (gamma * g)
                    caption_text = f"Calculated using Schulze Eq. 10.6a: $b_{{crit}} = \\sigma_{{c,crit}} / (\\rho_b \\cdot g) = {sigma_c_crit_pa:.1f} Pa / ({gamma} \\cdot {g})$"

                st.success(f"**Required Hopper Angle ($\\Theta$):** Steeper than **{theta_prime:.1f}°** from vertical.")
                st.success(f"**Minimum Outlet Dimension (B or d):** **{B_min:.2f} m**")
                st.caption(caption_text)
            
            except Exception as e:
                st.error(f"An error occurred during Mass-Flow calculation: {e}")

        with results_cols[1]:
            st.subheader("Flow Function vs. Flow Factor Plot")
            sigma_1_plot_max = max(sigma_1_plot_max_base, locals().get("sigma_1_crit_kpa", 0)) * 1.5
            sigma_1_plot = np.linspace(0, sigma_1_plot_max, 50)
            
            fig, ax = plt.subplots()
            ax.plot(sigma_1_plot, ff_inst_func(sigma_1_plot), label="Instantaneous FF (t=0)")
            ax.plot(sigma_1_plot, ff_time_func(sigma_1_plot), label="Time FF (t>0) (Design)", linestyle='--', color='red')
            
            if 'ff_value' in locals() and 'sigma_1_crit_kpa' in locals():
                ax.plot(sigma_1_plot, ff_line_func(sigma_1_plot), label=f"Hopper Flow Factor ($ff = {ff_value:.2f}$)", color='green')
                ax.plot(sigma_1_crit_kpa, sigma_c_crit_kpa, 'ro', label=f"Design Point ($\\sigma_{{c,crit}} = {sigma_c_crit_kpa:.1f}$ kPa)")
                ax.vlines(sigma_1_crit_kpa, 0, sigma_c_crit_kpa, colors='gray', linestyles='dotted')
                ax.hlines(sigma_c_crit_kpa, 0, sigma_1_crit_kpa, colors='gray', linestyles='dotted')
            
            ax.set_xlabel("Consolidation Stress ($\\sigma_1$) [kPa]")
            ax.set_ylabel("Unconfined Yield Strength ($\\sigma_c$) [kPa]")
            ax.set_title(f"Mass-Flow Design for {solid_name}")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)
            st.pyplot(fig)

    # --- Funnel-Flow Calculation ---
    elif flow_pattern == "Funnel-Flow":
        with results_cols[0]:
            st.subheader("Funnel-Flow Design (Schulze 10.3.2)")
            ff_design_func = ff_time_func 

            # 1. Complete Clearance Check
            st.markdown("#### 1. Complete Clearance (Schulze 10.3.2.1)")
            theta_cd = 65.0 - phi_prime_calc
            st.metric(label="Max. Hopper Angle ($\\Theta_{cd}$) for Complete Clearance", value=f"≤ {theta_cd:.1f}°")
            st.caption(f"To ensure gravity emptying, hopper angle must be steeper than this. (Est. $\\Theta_{{cd}} < 65^\circ - \\phi_x = 65^\circ - {phi_prime_calc:.1f}^\circ$)")

            st.markdown("#### 2. No-Ratholing (Piping) [Schulze 10.3.2.2]")
            
            try:
                # --- Calculate Lower Bound (Emptying) ---
                st.info("Calculating **Lower Bound (Emptying)** condition.")
                phi_lin_approx_lower = get_phi_lin(delta) 
                f_phi_i_val_lower = get_f_phi_i(phi_lin_approx_lower)
                
                ff_p = get_flow_factor_ffp(delta, phi_lin_approx_lower, f_phi_i_val_lower)
                ffp_line_func = lambda sigma_1: sigma_1 / ff_p
                
                intersection_func_lower = lambda sigma_1: ff_design_func(sigma_1) - ffp_line_func(sigma_1)
                sigma_1_crit_kpa_lower = fsolve(intersection_func_lower, sigma_1_plot_max_base / 2)[0]
                sigma_c_crit_kpa_lower = ff_design_func(sigma_1_crit_kpa_lower)
                f_phi_i_lower = f_phi_i_val_lower
                
                # Convert to Pa for physics equation
                D_crit_lower = f_phi_i_lower * (sigma_c_crit_kpa_lower * 1000) / (gamma * g) 
                
                st.metric("Min. Ratholing Dimension ($D_{crit, lower}$)", f"{D_crit_lower:.2f} m")
                st.caption(
                    f"Intermediate values (Lower Bound):\n"
                    f"- $\\phi_{{lin, approx}} = {phi_lin_approx_lower:.1f}^\circ$ (used as $\\phi_i$)\n"
                    f"- $f(\\phi_i) = {f_phi_i_lower:.2f}$ (from Fig. 10.19)\n"
                    f"- $ff_p = {ff_p:.2f}$ (from Eq. 10.11)\n"
                    f"- $\\sigma_{{1,crit}} = {sigma_1_crit_kpa_lower:.1f}$ kPa, $\\sigma_{{c,crit}} = {sigma_c_crit_kpa_lower:.1f}$ kPa"
                )
                
                # --- Calculate Upper Bound (Filling) ---
                st.info("Calculating **Upper Bound (Filling)** condition. [Schulze 10.3.2.4]")
                
                if hopper_shape == 'Conical':
                    A_silo = np.pi * (D_silo/2)**2
                    U_silo = np.pi * D_silo
                else: 
                    st.warning("Janssen calculation for Plane-Flow is simplified, using circular (D) logic.")
                    A_silo = np.pi * (D_silo/2)**2 
                    U_silo = np.pi * D_silo       

                phi_x_rad = np.radians(phi_prime_calc)
                
                # Janssen Equation (Pa)
                term_in_exp = -K_janssen * np.tan(phi_x_rad) * U_silo * h_f / A_silo
                sigma_v_max_pa = (gamma * g * A_silo / (K_janssen * np.tan(phi_x_rad) * U_silo)) * (1 - np.exp(term_in_exp))
                
                # Convert to kPa for FF
                sigma_1_crit_kpa_upper = sigma_v_max_pa / 1000
                sigma_c_crit_kpa_upper = ff_design_func(sigma_1_crit_kpa_upper)
                
                phi_lin_crit_upper = get_phi_lin(delta) 
                f_phi_i_upper = get_f_phi_i(phi_lin_crit_upper)
                
                # Convert to Pa for physics equation
                D_crit_upper = f_phi_i_upper * (sigma_c_crit_kpa_upper * 1000) / (gamma * g)
                
                st.metric("Min. Ratholing Dimension ($D_{crit, upper}$)", f"{D_crit_upper:.2f} m")
                
                if D_crit_upper > D_silo:
                    st.warning(f"**Note:** The 'Upper Bound' rathole dimension ({D_crit_upper:.2f} m) is larger than the silo diameter ({D_silo:.1f} m). This suggests the calculation may be too conservative, or that ratholing is a very high risk for this fill height.")
                
                st.caption(
                    f"Intermediate values (Upper Bound):\n"
                    f"- Max. vertical stress $\\sigma_{{v,max}} = \\sigma_{{1,crit}} = {sigma_1_crit_kpa_upper:.1f}$ kPa (from Janssen)\n"
                    f"- Resulting $\\sigma_{{c,crit}} = {sigma_c_crit_kpa_upper:.1f}$ kPa (from FF)\n"
                    f"- $f(\\phi_i) = {f_phi_i_upper:.2f}$ (from Fig. 10.19)"
                )
                
                B_crit = 0.0 

                if hopper_shape == "Plane-Flow (Slot)":
                    st.markdown("#### 3. No-Doming (Slot Outlet) [Schulze 10.3.2.5]")
                    ff_doming = 1.7
                    ff_line_func_doming = lambda sigma_1: sigma_1 / ff_doming
                    
                    intersection_func_doming = lambda sigma_1: ff_design_func(sigma_1) - ff_line_func_doming(sigma_1)
                    sigma_1_crit_kpa_doming = fsolve(intersection_func_doming, sigma_1_plot_max_base / 2)[0]
                    sigma_c_crit_kpa_doming = ff_design_func(sigma_1_crit_kpa_doming)
                    
                    H_theta_doming = 1.15
                    # Convert to Pa for physics equation
                    B_crit = H_theta_doming * (sigma_c_crit_kpa_doming * 1000) / (gamma * g) 
                    
                    st.metric("Minimum Minor Dimension ($b_{crit}$) (No-Doming)", f"{B_crit:.2f} m")
                    st.caption(
                        f"Intermediate values (Doming):\n"
                        f"- $\\sigma_{{1,crit,doming}} = {sigma_1_crit_kpa_doming:.1f}$ kPa, $\\sigma_{{c,crit,doming}} = {sigma_c_crit_kpa_doming:.1f}$ kPa"
                    )
                
                st.markdown("#### 4. Final Funnel-Flow Design")
                final_crit_dim = max(D_crit_lower, D_crit_upper, B_crit)
                if hopper_shape == "Conical":
                    st.error(f"**Final Outlet Diameter ($d$) must be > {final_crit_dim:.2f} m** (the larger of the Upper and Lower Bound rathole diameters).")
                else: # Plane-Flow
                    st.error(f"**Final Outlet Slot must be > {final_crit_dim:.2f} m (Diagonal) AND > {B_crit:.2f} m (Width).** The controlling dimension is the largest of all checks.")

            except Exception as e:
                st.error(f"An error occurred during Funnel-Flow calculation: {e}")

        with results_cols[1]:
            st.subheader("Funnel-Flow Ratholing Plot")
            
            # Determine plot range
            plot_max_stress = sigma_1_plot_max_base
            if 'sigma_1_crit_kpa_lower' in locals():
                 plot_max_stress = max(plot_max_stress, sigma_1_crit_kpa_lower, sigma_1_crit_kpa_upper)
            sigma_1_plot_max = plot_max_stress * 1.5
            sigma_1_plot = np.linspace(0, sigma_1_plot_max, 50)
            
            fig, ax = plt.subplots()
            ax.plot(sigma_1_plot, ff_inst_func(sigma_1_plot), label="Instantaneous FF (t=0)")
            ax.plot(sigma_1_plot, ff_time_func(sigma_1_plot), label="Time FF (t>0) (Design)", linestyle='--', color='red')
            
            if 'sigma_1_crit_kpa_lower' in locals():
                # Plot Lower Bound
                ax.plot(sigma_1_plot, ffp_line_func(sigma_1_plot), label=f"$ff_p = {ff_p:.2f}$ (Lower Bound)", color='green')
                ax.plot(sigma_1_crit_kpa_lower, sigma_c_crit_kpa_lower, 'go', label=f"Lower Bound $\\sigma_{{c,crit}} = {sigma_c_crit_kpa_lower:.1f}$ kPa")
                
                # Plot Upper Bound
                ax.axvline(sigma_1_crit_kpa_upper, label=f"Upper Bound $\\sigma_{{1,crit}} = {sigma_1_crit_kpa_upper:.1f}$ kPa", color='purple', linestyle='dashed')
                ax.plot(sigma_1_crit_kpa_upper, sigma_c_crit_kpa_upper, 'mP', markersize=8, label=f"Upper Bound $\\sigma_{{c,crit}} = {sigma_c_crit_kpa_upper:.1f}$ kPa")

            
            ax.set_xlabel("Consolidation Stress ($\\sigma_1$) [kPa]")
            ax.set_ylabel("Unconfined Yield Strength ($\\sigma_c$) [kPa]")
            ax.set_title(f"Funnel-Flow Ratholing for {solid_name}")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)
            st.pyplot(fig)