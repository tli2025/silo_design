import matplotlib.pyplot as plt
import numpy as np

# We can import the data directly from your app_utils file
from app_utils import CONICAL_BOUNDARY_POINTS, CONICAL_FF_POINTS

print("Generating verification plot for Figure 10.31...")

# 1. Filter the data for phi_e = 30°
phi_e_to_plot = 30
boundary_data = CONICAL_BOUNDARY_POINTS[CONICAL_BOUNDARY_POINTS[:, 0] == phi_e_to_plot]
ff_data = CONICAL_FF_POINTS[CONICAL_FF_POINTS[:, 0] == phi_e_to_plot]

# 2. Create a new plot that mimics the style of the book's chart
plt.figure(figsize=(9, 7))

# 3. Plot the Mass Flow Boundary
# x-axis is theta (column 2), y-axis is phi_x (column 1)
# Sort by theta for correct plotting
boundary_data = boundary_data[boundary_data[:, 2].argsort()]
plt.plot(boundary_data[:, 2], boundary_data[:, 1], 'o--', label='Mass Flow Boundary ($\phi_e$=30°)')

# 4. Plot the ff contours that are ACTUALLY in Fig 10.31
ff_values_to_plot = [1.5, 1.6, 1.8, 2.0, 2.5, 3.0, 4.0]

for ff in ff_values_to_plot:
    ff_subset = ff_data[ff_data[:, 3] == ff]
    # Sort by theta to ensure the line plots correctly
    # The "A" loops are already sorted in order, so this is fine
    ff_subset = ff_subset[ff_subset[:, 2].argsort()]
    
    # Special case for the "A" loops which are closed
    if ff == 1.5 or ff == 1.6:
        # Close the loop by appending the first point
        loop_data = np.vstack([ff_subset, ff_subset[0]])
        plt.plot(loop_data[:, 2], loop_data[:, 1], 's-', label=f'ff = {ff} (Loop A)')
    else:
        plt.plot(ff_subset[:, 2], ff_subset[:, 1], 's-', label=f'ff = {ff}')


# 5. Set up the chart to match Figure 10.31
plt.title('Verification Plot for CORRECTED Data\n(Compare to Fig. 10.31 for Conical, $\phi_e = 30^\circ$)')
plt.xlabel('Hopper Wall Inclination $\Theta_c$ [°]')
plt.ylabel('Wall Friction Angle $\phi_x$ [°]')

# Set axis limits to match the original chart
plt.xlim(0, 60)
plt.ylim(0, 40)
plt.xticks(np.arange(0, 61, 10))
plt.yticks(np.arange(0, 41, 5))

plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.gca().invert_xaxis() # Invert X-axis to match the style of some charts (optional, but good for comparison)
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

# 6. Save the plot to a file
output_filename = 'digitized_data_fig_10_31_CORRECTED.png'
plt.savefig(output_filename)

print(f"✅ Success! Verification plot saved as '{output_filename}'")
print("Please open this file and compare it to your 'assets/fig_10_31.png' to verify.")