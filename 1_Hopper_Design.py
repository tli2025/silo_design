import streamlit as st

st.set_page_config(
    page_title="Hopper Design Fundamentals",
    page_icon="🏗️",
    layout="wide"
)

st.title("Hopper Design Fundamentals 🏗️")
st.markdown("This app provides an overview and calculation tool for silo hopper design based on the methods described by A. W. Jenike and D. Schulze.")
st.info("Navigate to the app's pages using the **sidebar on the left**.")

st.header("Fundamentals of Hopper Design for Flow")
st.markdown("This page summarizes the core principles from 'Powders and Bulk Solids' (Schulze, 2021).")

# --- Section 1: Flow Patterns ---
st.subheader("1. The Two Silo Flow Patterns")
st.markdown(
    """
    When a bulk solid is discharged from a silo, it will flow in one of two ways: **Funnel Flow** or **Mass Flow**. The entire purpose of hopper design is to achieve the correct pattern for your material.
    """
)

st.image(
    "assets/fig_10_1.png",
    caption="Fig. 1: (a) Mass Flow, where all material is in motion. (b, c, d) Funnel Flow, showing stagnant, non-moving zones.",
    width=550
)

st.markdown(
    """
    #### Funnel Flow (also called Core Flow)
    * **What it is:** Only a central channel of the solid moves during discharge. The material near the walls remains stationary in "stagnant zones" (or "dead zones").
    * **Flow Pattern:** First-In, Last-Out (FILO).
    * **Problems:** This is the default and most problematic pattern. It leads to:
        * **Arching (Doming):** A stable arch of solid forms over the outlet, stopping all flow.
        * **Ratholing (Piping):** The central core empties completely, leaving a stable, empty hole. The material in the stagnant zone will not discharge.
        * **Segregation:** If you fill the silo with a mix of fine and coarse particles, the fines typically concentrate in the center. Funnel flow will discharge *only the fines* first, then *only the coarse* last.
    
    #### Mass Flow
    * **What it is:** The entire contents of the silo, including the material at the walls, is in motion whenever any solid is withdrawn.
    * **Flow Pattern:** First-In, First-Out (FIFO). This ensures a predictable residence time.
    * **How to achieve it:** The hopper walls must be **steep enough** and **low-friction enough** for the specific solid being stored.
    * **Benefits:** Mass flow is the reliable, engineered solution. It **prevents ratholing and caking**. It also **remixes** the material as it flows, which drastically reduces segregation problems.
    """
)
st.image(
    "assets/fig_1_2.png",
    caption="Fig. 2: Common flow problems, including (a) Arching, (c) Ratholing, and (e) Segregation, which are typical of Funnel Flow.",
    width=550
)

st.markdown("---")

# --- Section 2: What Causes Flow Problems? ---
st.subheader("2. What Causes Flow Problems? (The Solid's Strength)")
st.markdown(
    """
    Flow problems (arching and ratholing) happen when the **strength of the bulk solid** is greater than the **stress trying to make it flow**.
    
    The most important concept in bulk solids is that their strength is not fixed. **A solid's strength depends on how much it has been consolidated (squeezed).**
    
    * A loose powder has no strength.
    * When you put it in a silo, the weight of the material above consolidates it, making it gain strength.
    * This consolidation strength is what allows the solid to form a stable arch.
    
    To design a hopper, we must measure two key properties:
    1.  **Cohesive Strength:** The inherent strength of the solid, which we measure as the **Unconfined Yield Strength ($\sigma_c$)**.
    2.  **Wall Friction ($\phi_x$):** The friction between the bulk solid and the hopper wall material. This determines if the solid will slide on the wall (Mass Flow) or stick (Funnel Flow).
    """
)

st.markdown("---")

# --- Section 3: How We Measure Flow Properties ---
st.subheader("3. How We Measure Flow Properties (Shear Testing)")
st.markdown(
    """
    These properties are measured using a **Shear Tester**. The two most common types are the Jenike Shear Tester and the Schulze Ring Shear Tester.
    """
)

# *** UPDATED SECTION: Removed st.columns ***
st.markdown("#### The Jenike Shear Tester")
st.image("assets/fig_4_3.png", caption="Fig. 3: Principle of the Jenike shear cell, a translational (linear) tester.", width=550)
st.markdown("This tester pushes a ring of material linearly across a base to measure the shear force.")

st.markdown("#### The Ring Shear Tester")
st.image("assets/fig_4_9.png", caption="Fig. 4: Shear cell of the Schulze ring shear tester, a rotational tester.", width=550)
st.markdown("This tester rotates an annular (ring-shaped) trough of material under a stationary lid to measure the shear torque.")
# *** END OF UPDATE ***

#    The flow function shows the relationship between the consolidation stress ($\sigma_1$) and unconfined yield strength ($\sigma_c$). Flowability of a bulk solid is characterized mainly the flow function and the ratio of consolidation stress, $\sigma_1$, to unconfined yield strength, $\sigma_c$, called $\{ff}_c$ is used to characterize flowability numerically.
st.markdown(
    """
    Both testers work on the same two-step principle to get a single point on the solid's "Flow Function":
    
    1.  **Step 1: Preshear (Consolidation)**
        A sample is sheared under a constant normal stress ($\sigma_{pre}$) until it reaches a constant, steady flow. This creates a uniform, "critically consolidated" sample.
    
    2.  **Step 2: Shear to Failure**
        The normal stress is *lowered* ($\sigma_{sh} < \sigma_{pre}$ ) and the sample is sheared again until it breaks or "fails". The peak shear stress ($\\tau_{sh}$) is recorded.
    """
)
st.markdown("---")

# --- Section 4: The Result: The Flow Function ---
st.subheader("4. The Result: The Flow Function")
st.markdown(
    """
    The pairs of shear points ($\sigma_{sh}$, $\\tau_{sh}$) from Step 2 are plotted to create a **Yield Locus**.
    
    As shown in the figure below, we use **Mohr's Circles** on this Yield Locus to find two critical values:
    
    * **Consolidation Stress ($\sigma_1$):** A Mohr circle is drawn tangent to the Yield Locus and passing through the preshear point. Its major principal stress is the $\sigma_1$ for this test.
    * **Unconfined Yield Strength ($\sigma_c$):** A second Mohr circle is drawn tangent to the Yield Locus and passing through the origin (0,0). Its major principal stress is the strength, $\sigma_c$.
    """
)
st.image(
    "assets/fig_3_13.png",
    caption="Fig. 5: How a Yield Locus (measured from shear points) is used to find both the Consolidation Stress (σ1) and the Unconfined Yield Strength (σc) using Mohr's circles.",
    width=550
)

st.markdown(
    """
    This pair of ($\sigma_1$, $\sigma_c$) values is just **one point on the Flow Function**. The entire 2-step test is repeated at different consolidation stresses to get more points and build the complete **Flow Function**, which is the final, critical plot for our design.
    
    Finally, if a solid can cake or gain strength over time, we must also measure its **Time Flow Function**. This is done by letting the sample sit under the consolidation load for a set period (e.g., 2 days) before shearing it to failure. This Time Flow Function is almost always used for the final design to ensure the hopper will work even after a weekend shutdown.
    """
)