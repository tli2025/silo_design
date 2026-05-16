import matplotlib.pyplot as plt
import numpy as np

from app_utils import f_phi_i_data, get_f_phi_i


def main():
    """Generate a simple verification plot for the current f(phi_i) data."""
    phi_values = np.linspace(
        min(f_phi_i_data["phi_i"]),
        max(f_phi_i_data["phi_i"]),
        100,
    )
    f_values = [get_f_phi_i(phi, show_message=False) for phi in phi_values]

    plt.figure(figsize=(8, 5))
    plt.plot(phi_values, f_values, label="Interpolated f(phi_i)")
    plt.plot(f_phi_i_data["phi_i"], f_phi_i_data["f"], "o", label="Digitized points")
    plt.xlabel("Internal friction angle phi_i [deg]")
    plt.ylabel("f(phi_i)")
    plt.title("Verification Plot for Schulze Fig. 10.19 Digitized Data")
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend()

    output_filename = "digitized_f_phi_i_verification.png"
    plt.savefig(output_filename, dpi=150, bbox_inches="tight")
    print(f"Verification plot saved as '{output_filename}'.")


if __name__ == "__main__":
    main()
