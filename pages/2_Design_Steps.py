import streamlit as st

st.set_page_config(
    page_title="Hopper Design Steps",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Hopper Design Steps")
st.markdown("This page describe the key design procedure for silo/hopper design follows the logic established by Jenike and described in Schulze (2021), Chapter 10. It aims to provide a quick overview of the key steps in the design process which can be followed for a quick design evaluation.")

# --- Flowchart Section ---
st.subheader("Hopper Design Flowchart")
st.markdown(
    """
    > **START: Get Project Requirements**
    > 1.  What is the bulk solid?
    > 2.  What is the required storage time (e.g., 2 days)?
    > 3.  What are the environmental conditions (temperature, humidity)?
    >
    > **STEP 1: Characterize the Bulk Solid (Lab Tests)**
    > * Perform shear tests on a representative sample.
    > * **Outputs:**
    >     1.  **Flow Function (FF)** (Instantaneous and Time)
    >     2.  **Wall Yield Locus (WYL)** for a chosen wall material
    >     3.  **Effective Angle of Internal Friction ($\\phi_e$)**
    >     4.  **Bulk Density ($\\rho_b$)**
    >
    > **STEP 2: Select Flow Pattern**
    > * Is the solid cohesive, segregating, or time-sensitive?
    > * **YES** $\\rightarrow$ Choose **Mass Flow** (Recommended).
    > * **NO** $\\rightarrow$ **Funnel Flow** may be acceptable.
    >
    > **STEP 3: Select Hopper Geometry**
    > * Choose the basic hopper shape: **Conical** (circular outlet) or **Wedge/Plane-Flow** (slotted outlet).
    >
    > **STEP 4: Calculate Hopper Angle & Outlet Size**
    > * **IF MASS FLOW:**
    >     1.  Find max. Hopper Angle ($\\Theta$) from charts (e.g., Fig. 6).
    >     2.  Find Flow Factor ($ff$) from the same chart.
    >     3.  Find critical strength ($\\sigma_{c,crit}$) by intersecting $ff$ and the Time Flow Function.
    >     4.  Calculate minimum outlet dimension **$d_{crit}$** (for arching).
    > * **IF FUNNEL FLOW:**
    >     1.  Ensure **Complete Clearance**: Hopper angle ($\\Theta$) must be steep enough for the silo to empty completely by gravity. (e.g., for cohesive solids, Schulze suggests $\\Theta_{cd} < 65^\\circ - \\phi_x$ ).
    >     2.  Calculate critical rathole dimension **$D_{crit}$** (using $ff_p$ or Janssen method). This prevents piping.
    >     3.  *If outlet is a slot*, calculate minimum width **$b_{crit}$** (for arching, using $ff=1.7$).
    >     4.  The final outlet must be larger than *both* $D_{crit}$ and $b_{crit}$.
    >
    > **STEP 5: Consider Vertical Section (Cylinder)**
    > * Calculate structural loads (stresses) on the vertical walls using the Janssen equation, which is also an input for the Funnel Flow (Upper Bound) calculation.
    >
    > **END: Final Design**
    > * Hopper Angle: $\\Theta$
    > * Outlet Dimension: $d_{crit}$ (or $b_{crit}$ / $L$)
    > * Select an appropriate feeder (e.g., increasing capacity)
    """
)
st.markdown("---")

# --- Detailed Steps Section ---

st.subheader("Objective")
st.markdown(
    """
    The goal of the design process is to determine the **hopper wall inclination ($\\Theta$)** necessary for mass flow and the **minimum outlet size ($d_{crit}$ or $b_{crit}$)** to prevent flow problems due to arching or ratholing.
    """
)

st.subheader("Step 1: Characterize the Bulk Solid")
st.markdown(
    """
    Before any design can begin, you must measure the physical properties of your *specific* bulk solid using a shear tester. These measurements provide the essential parameters for the design calculations.
    
    Essentially, four key properties are determined:
    
    1.  **Unconfined Yield Strength ($\\sigma_c$):** This is the cohesive strength the solid gains after being consolidated. It is the **decisive property for preventing arching**. This is not a single value, but is plotted as a **Flow Function (FF)**, which shows how strength ($\\sigma_c$) increases with consolidation stress ($\\sigma_1$).
    
    2.  **Angle of Wall Friction ($\\phi_x$):** This measures the friction between the bulk solid and a specific wall material (e.g., stainless steel, TIVAR 88). It is the **major property for determining the hopper angle for mass flow**.
        
    3.  **Effective Angle of Internal Friction ($\\phi_e$):** This characterizes the internal friction of the bulk solid as it flows against itself.
    
    4.  **Bulk Density ($\\rho_b$):** This is the density of the solid at a given consolidation stress.
    
    For solids that may cake or gain strength over time, the **Time Flow Function** (FFt) must also be measured (Fig. 1) to account for storage at rest (e.g., over a weekend), as this strength is typically used for the design. While the **Instantaneous Flow Function** represents the strength during continuous flow.

    The wall friction angle, $\\phi_x$, is the slope of a line running from the origin of the $\\sigma_w$, $\\tau_w$ diagram to a point on the wall yield locus (Fig. 2). The wall friction angle could be constant or stress dependent and it is important to accurately account for it during the silo design.
    """
)


st.image("assets/fig_3_3.png", caption="Fig. 1: Example of Instantaneous Flow Function (A) and Time Flow Functions (A1, A2) showing strength gain from caking.", width=550)
st.image("assets/fig_3_26.png", caption="Fig. 2: Example of a Wall Yield Locus (WYL). The slope of the line from the origin gives the wall friction angle $\\phi_x$.", width=550)


st.subheader("Step 2: Select a Flow Pattern")
st.markdown(
    """
    You must choose between **Mass Flow** (first-in, first-out) or **Funnel Flow** (first-in, last-out). 
    
    **Mass flow** is required for cohesive, segregating, or time-sensitive products. 
    
    **Funnel flow**, despite its many shortcomings, is still widely used. This type of design is only suitable for **free-flowing, coarse materials** where the product is **non-degrading and insensitive to segregation** (e.g., gravel, sand, plastic pellets).
    """
)
st.image("assets/fig_10_1.png", caption="Fig. 3: (a) Mass Flow vs. (b, c, d) Funnel Flow.", width=550)

st.subheader("Step 3: Select Hopper Geometry")
st.markdown(
    """
    The two basic hopper shapes are **Conical** (circular outlet) and **Wedge-shaped** (slotted outlet, also called plane-flow). Wedge-shaped hoppers can be designed with less steep walls (larger $\\Theta_p$) than conical hoppers for the same material.
    
    Other common shapes, like **Pyramidal** hoppers (square outlets), are generally treated as conical hoppers for design purposes, but they are *less* favorable for mass flow because the valleys are an obstruction.
    """
)
st.image("assets/fig_10_4.png", caption="Fig. 4: Basic symmetric hopper shapes: (a) Conical and (b) Wedge-shaped.", width=550)
st.image("assets/fig_11_3.png", caption="Fig. 5: Other hopper configurations, such as (a) Cylinder-to-wedge and (c) Pyramidal.", width=550)


st.subheader("Step 4: Perform Design Calculations")
st.markdown("The calculations depend on the flow pattern you selected.")

st.markdown("#### If Mass-Flow is Selected (Schulze 10.3.1):")
st.markdown(
    """
    **1. Find Hopper Angle ($\\Theta$):**
    
    This step involves using the **Mass Flow Diagrams** (like Figs. 6 and 7 below). These charts plot the **Hopper Wall Inclination ($\\Theta$)** (from vertical) versus the **Wall Friction Angle ($\\phi_x$)**. The book provides a different chart for each **Effective Angle of Internal Friction ($\\phi_e$)**.
    
    In these figures, the "mass flow region" shows the combinations of $\\Theta$ and $\\phi_x$ that will result in mass flow. This region is separated from the "funnel flow region" by the **mass flow boundary** (heavy dashed line). These boundaries depend on the solid's effective angle of internal friction, $\\phi_e$.
    
    You find the chart that matches your solid's $\\phi_e$ (e.g., $\\phi_e = 40^\\circ$), find your measured $\\phi_x$ (e.g., $20^\\circ$) on the y-axis, move to the boundary line, and read the maximum $\\Theta$ on the x-axis. Your hopper *must* be steeper than this value (a smaller $\\Theta$).
    
    **Important:** For the case of a conical hopper, a **safety margin of 3° to 5°** should be subtracted from the maximum inclination because the mass flow boundaries have been calculated for ideal conditions.
    """
)

st.image("assets/fig_10_6.png", caption="Fig. 6: Mass flow boundaries for CONICAL hoppers (example for $\\phi_e = 40^\\circ$).", width=550)
st.image("assets/fig_10_7.png", caption="Fig. 7: Mass flow boundaries for WEDGE-SHAPED hoppers (example for $\\phi_e = 40^\\circ$ and $50^\\circ$).", width=550)

st.markdown(
    """
    **2. Find Flow Factor ($ff$):**

    For the practical determination of critical outlet dimensions, you need to find the **flow factor ($ff$)** value for your chosen design point.
    The flow factor $ff$ is dependent on the flow properties ($\\phi_x$, $\\phi_e$) and the hopper shape. Jenike provided diagrams for an easy determination of the flow factor. Each of the
    diagrams is valid for a specific hopper geometry (e.g., conical) and a fixed value of the
    effective angle of internal friction, $\\phi_e$. Two of these diagrams are shown in Figs. 8
    and 9. The solid curves represent constant values of $ff$, as given by the labels.
    """
)

st.image("assets/fig_10_31.png", caption="Fig. 8: Flow factor, $ff$, for CONICAL hoppers (example for $\\phi_e = 30^\\circ$).", width=550)   
st.image("assets/fig_10_39.png", caption="Fig. 9: Flow factor, $ff$, for WEDGE-SHAPED hoppers (example for $\\phi_e = 30^\\circ$).", width=550)               

st.markdown(
    """    
    **3. Calculate Outlet Dimension ($d_{crit}$ or $b_{crit}$):**
    
    Now you plot your solid's **Time Flow Function** and the **Flow Factor Line** (a line from the origin with a slope of $1/ff$, as shown in Fig. 10). The intersection of these two lines gives the **critical unconfined yield strength ($\\sigma_{c,crit}$)**.
    
    Finally, you calculate the minimum outlet dimension. A simple approximation is $d_{crit} = 2 \\cdot \\sigma_{c,crit} / (g \\cdot \\rho_b)$ for a conical hopper and $b_{crit} = \\sigma_{c,crit} / (g \\cdot \\rho_b)$ for a wedge-shape hopper.
    
    A more precise calculation by Jenike and Leser uses the function $H(\\Theta)$ from Fig. 11 to account for the hopper geometry: $d_{crit} = H(\\Theta) \\cdot \\sigma_{c,crit} / (g \\cdot \\rho_b)$.
    """
)

st.image("assets/fig_10_12.png", caption="Fig. 10: Finding the critical strength ($\\sigma_{c,crit}$) by intersecting the Time Flow Function with the hopper's Flow Factor ($ff$) line.", width=550)
st.image("assets/fig_10_13.png", caption="Fig. 11: Chart for finding the $H(\\Theta)$ value needed in the $d_{crit}$ calculation.", width=550)

st.markdown("<h6>An Important Note: The Iterative Design Process</h6>", unsafe_allow_html=True)
st.markdown(
    """
    In practice, this is often an iterative procedure. Both the hopper angle for mass flow ($\\Theta$) and the flow factor ($ff$) depend on the effective angle of internal friction ($\\phi_e$) and the angle of wall friction ($\\phi_x$), which are often stress-dependent.
    
    This creates a "chicken-and-egg" problem:
    
    1.  To find the outlet size, you need the flow factor ($ff$).
    2.  To find the flow factor, you need the hopper angle ($\\Theta$) and the friction angles ($\\phi_e$, $\\phi_x$).
    3.  But the friction angles depend on the stress at the outlet, which you don't know until you've calculated the outlet size.
    
    **The solution is to iterate:**
    
    * **Guess 1:** *Estimate* your friction angles ($\\phi_e$, $\\phi_x$) based on the expected stress range (e.g., from Fig. 2).
    * **Calculate 1:** Find your hopper angle ($\\Theta$), flow factor ($ff$), and the critical outlet dimension ($d_{crit}$) and its corresponding critical consolidation stress ($\\sigma_{1,crit}$).
    * **Check:** Go back to your lab data. Look up the *actual* friction angles ($\\phi_e$, $\\phi_x$) at the $\\sigma_{1,crit}$ you just calculated.
    * **Compare:** Are the new friction angles the same as your initial guess?
        * **If Yes:** Your design is complete and consistent.
        * **If No:** Use these new, more accurate friction angles and repeat the calculation. This is your "Guess 2".
    
    This process is repeated until the estimated values match the calculated values. This is especially important when using the Time Flow Function.
    """
)


st.markdown("#### If Funnel-Flow is Selected (Schulze 10.3.2):")
st.markdown(
    """
    You must design against two separate failure modes. The outlet must be larger than both dimensions.

    **1. Ensure Complete Clearance :**
    First, you must ensure the hopper walls are steep enough for the silo to empty completely by gravity when it is "empty". If the walls are too shallow, material will remain in stagnant zones permanently.
    * For cohesive bulk solids, Schulze suggests a rough estimate for the maximum hopper inclination from vertical ($\\Theta_{cd}$) is: $\\Theta_{cd} < 65^\\circ - \\phi_x$.
    
    **2. Find Ratholing Dimension ($D_{crit}$) :**
    This calculation determines the largest stable "pipe" the material can form. You can use two methods. In both methods, the final critical diameter ($D_{crit}$) is found using this formula:
    
    $$D_{crit} = f(\\phi_i) \\cdot \\frac{\\sigma_{c,crit}}{g \\cdot \\rho_b}$$
    
    The value for $f(\\phi_i)$ is found from the chart in Fig. 13, using the solid's angle of internal friction. The methods differ in how they find the critical strength, $\\sigma_{c,crit}$:

    * **Method A: Lower Bound (Emptying)**
        This method assumes stresses are independent of filling height. It uses a special "flow factor for ratholing" ($ff_p$).
        1.  Calculate $ff_p$ using the following equation: $ff_p = \\frac{1 + \sin \phi_e}{4 \cdot \sin \phi_e} \cdot f(\phi_i)$. (If $ff_p < 1.7$, use $ff_p = 1.7$).
        2.  Plot the line $\\sigma_1' = \\sigma_1 / ff_p$ on the Flow Function chart (see Fig. 12).
        3.  The intersection of this $ff_p$ line with your **Time Flow Function** gives you the **$\\sigma_{c,crit}$** value.
        4.  Use this $\\sigma_{c,crit}$ in the equation for $D_{crit}$ to find the critical rathole diameter.

    * **Method B: Upper Bound (Filling)**
        This method is more conservative and accounts for consolidation from the full height of the silo.
        1.  Use the **Janssen equation** to find the *maximum* consolidation stress ($\\sigma_{1,crit}$) at the bottom of the silo based on the filling height ($h_f$) as
            $$ \sigma_{1,crit} = \\frac{\\rho_b g A}{K \\tan\\phi_x U} \cdot (1 - e^{-K \\tan\\phi_x U h_f / A}) $$
        2.  Find the corresponding strength, **$\\sigma_{c,crit}$**, by finding the $\\sigma_c$ value on your **Time Flow Function** at the $\\sigma_1$ you just calculated (see Fig. 14 for the concept).
        3.  Use this $\\sigma_{c,crit}$ in the equation for $D_{crit}$ to find the critical rathole diameter.
    """
)

st.image("assets/fig_10_20.png", caption="Fig. 12: Finding $\\sigma_{c,crit}$ for the 'Lower Bound' ratholing calculation.", width=600)
st.image("assets/fig_10_19.png", caption="Fig. 13: Chart for finding the $f(\\phi_i)$ value needed in the $D_{crit}$ calculation.", width=550)
st.image("assets/fig_10_22.png", caption="Fig. 14: Finding $\\sigma_{c,crit}$ for the 'Upper Bound' ratholing calculation.", width=600)

st.markdown(
    """
    **3. Find Arching Dimension ($b_{crit}$) :**
    Since for a conical funnel flow hopper the critical outlet diameter to avoid ratholing is always larger than the one to avoid arching, only a design to avoid
    ratholing is necessary. This check is required for non-circular (slot) outlets. Use the fixed **Flow Factor $ff = 1.7$** and find its intersection with your Time Flow Function. Calculate $b_{crit}$ using the arching equation (with $H(\\Theta) \\approx 1.15$).
    """
)
st.markdown("---")
st.subheader("Step 5: Design of the Vertical Section (Cylinder)")
st.markdown(
    """
    The vertical (cylindrical) section of the silo also requires design, primarily for structural loads. The stresses in this section are calculated using the **Janssen equation**.     
    This equation shows that, unlike a liquid (where pressure increases linearly with depth), the stress in a bulk solid increases non-linearly and approaches a **maximum asymptotic value** (Fig. 15). This happens because the silo wall supports a portion of the bulk solid's weight via wall friction.
    
    The key inputs for this calculation are:
    * **Silo Diameter ($D$)**
    * **Filling Height ($h_f$)**
    * **Bulk Density ($\\rho_b$)**
    * **Wall Friction Angle ($\\phi_x$)**
    * **Lateral Stress Ratio ($K$):** The ratio of horizontal to vertical stress (often assumed to be 0.4 or 0.5).
    
    The maximum stress from this calculation is critical for two reasons:
    1.  **Structural Design:** It determines the wall pressure for which the silo must be structurally designed to prevent failure.
    2.  **Funnel Flow Design:** It is the consolidation stress ($\\sigma_1$) used in the **"Upper Bound"** calculation for ratholing.

    The selection of diameter and height are manily affected by the plant layout, storage capacity, fabrication and shipping cost, etc. Usually $H/D$ should be between 1 and 4. Detailed design code should be followed and it is recommended to consult a professional firm or device vendor for support. 
    """
)
st.image("assets/fig_9_9.png", 
         caption="Fig. 15: Example of Janssen's equation, showing how vertical stress ($\\sigma_v$) increases to a maximum value based on wall friction ($\\phi_x$).",
         width=550)