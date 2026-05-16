# silo_design

A Streamlit app for preliminary silo and hopper design calculations for bulk solids. The app summarizes the Jenike/Schulze hopper design workflow and provides guided inputs for mass-flow and funnel-flow outlet sizing.

The current implementation is intended for engineering screening, training, and design review support. Final silo and feeder designs should still be checked against project data, applicable design codes, and qualified bulk-solids or structural engineering guidance.

## Main Functions

- Explains common silo flow patterns: mass flow, funnel flow, arching, ratholing, segregation, and caking.
- Walks through the hopper design procedure from material characterization to outlet sizing.
- Accepts measured or fitted bulk-solids data:
  - bulk density, `rho_b`
  - effective angle of internal friction, `phi_e`
  - wall yield locus data or a wall-friction equation
  - instantaneous and time flow functions
  - selected flow pattern and hopper geometry
- Displays verification plots for wall friction and flow-function inputs.
- Shows the relevant Schulze/Jenike chart image for manual lookup of hopper angle and flow factor.
- Calculates mass-flow outlet dimensions using the time flow function and selected flow factor.
- Calculates funnel-flow checks for complete clearance and ratholing, including lower-bound and Janssen upper-bound estimates.
- Saves the last submitted inputs to `last_inputs.json` so a previous design case can be reloaded.

## App Structure

```text
silo_design/
|-- 1_Hopper_Design.py        # Streamlit home page and hopper-design background
|-- app_utils.py              # Shared interpolation and line-fitting helpers
|-- pages/
|   |-- 2_Design_Steps.py     # Design-method explanation and reference figures
|   |-- 3_User_Inputs.py      # User input form, data persistence, and plots
|   `-- 4_Results.py          # Mass-flow and funnel-flow calculations/results
|-- assets/                   # Reference figures used by the Streamlit pages
|-- last_inputs.json          # Saved example/latest input case
|-- requirements.txt          # Python dependencies
|-- test_utils.py             # Legacy/manual helper test script
`-- verify_digitization.py    # Legacy/manual digitized-chart verification script
```

## Download

Install Git if it is not already available, then clone the repository:

```powershell
git clone https://github.com/tli2025/silo_design.git
cd silo_design
```

If you already cloned the repository and just want the latest version:

```powershell
git pull
```

## Setup

Python 3.12 is recommended because the dependency versions in `requirements.txt` were captured from a Python 3.12 environment.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `python` is not on your PATH on Windows, use the Python launcher instead:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Run the App

Start Streamlit from the repository root:

```powershell
streamlit run 1_Hopper_Design.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in a browser. Use the sidebar to move through the pages.

## Basic Use

1. Open `1_Hopper_Design.py` in Streamlit to review the background on mass flow, funnel flow, shear testing, and flow functions.
2. Go to `Design Steps` for the full design sequence and reference figures.
3. Go to `User Inputs`.
4. Enter project information, bulk density, wall friction data, and flow-function data.
5. Select the intended flow pattern:
   - `Mass-Flow` for cohesive, segregating, or time-sensitive solids.
   - `Funnel-Flow` for suitable free-flowing materials where stagnant zones are acceptable.
6. Select hopper geometry:
   - `Conical`
   - `Plane-Flow (Slot)`
7. For mass-flow designs, use the displayed chart to manually enter:
   - design hopper angle from vertical
   - flow factor, `ff`
8. Click `Submit Data and Go to Results`.
9. Open `Results` from the sidebar to review calculated outlet dimensions and plots.

## Calculation Notes

The app uses stresses in kPa for input plots and converts to Pa for outlet-size equations. Bulk density is entered as kg/m3, and gravity is taken as `9.81 m/s2`.

For mass-flow designs, the app intersects the time flow function with the selected flow-factor line and estimates the minimum outlet dimension:

- conical hopper: `d_crit = 2 * sigma_c,crit / (rho_b * g)`
- plane-flow slot: `b_crit = sigma_c,crit / (rho_b * g)`

For funnel-flow designs, the app evaluates:

- complete-clearance angle estimate: `Theta_cd < 65 deg - phi_x`
- lower-bound ratholing dimension using `ff_p`
- upper-bound ratholing dimension using a Janssen stress estimate
- slot-outlet doming check when using plane-flow geometry

Some chart lookups are still manual. The app displays the relevant figure and asks the user to enter the hopper angle and flow factor read from the chart.

## Data Persistence

The input page writes submitted data to:

```text
last_inputs.json
```

Use `Load Last Inputs` on the input page to restore the saved case.

## Development Notes

You can check Python syntax with:

```powershell
python -m py_compile 1_Hopper_Design.py app_utils.py pages\2_Design_Steps.py pages\3_User_Inputs.py pages\4_Results.py
```

Run the lightweight utility checks with:

```powershell
python -B test_utils.py
```

To regenerate the interpolation verification plot for the current `f(phi_i)` digitized data:

```powershell
python -B verify_digitization.py
```

## References

The app text and calculations are based on hopper-design methods described by Jenike and Schulze, especially the flow-function, wall-friction, mass-flow, arching, ratholing, and Janssen-equation design concepts used in bulk-solids handling.
