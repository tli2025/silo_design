import numpy as np
from app_utils import (
    get_H_function, 
    get_hopper_angle_theta, 
    get_flow_factor_ff,
    get_f_phi_i,
    get_flow_factor_ffp,
    get_phi_lin
)

# --- Define Helper for Testing ---
def run_test(test_name, expected, actual, tolerance=0.5):
    """Simple test runner"""
    error = abs(expected - actual)
    if error <= tolerance:
        print(f"✅ PASS: {test_name}")
    else:
        print(f"❌ FAIL: {test_name}")
        print(f"   Expected: {expected}, Got: {actual} (Error: {error})")

def run_ffp_test(test_name, expected, actual, tolerance=0.1):
    """Test runner for ffp which has a floor value"""
    if actual < 1.7:
        print(f"❌ FAIL: {test_name}")
        print(f"   Expected: {expected} (>=1.7), Got: {actual} (Error: {abs(expected-actual)})")
    else:
        run_test(test_name, expected, actual, tolerance)


print("--- Starting Test Run ---")

# --- Test H(Θ) Function (Fig. 10.13) ---
print("\n## Testing H(Θ) Function ##")
run_test("H(Θ) Conical @ 20°", 2.29, get_H_function(20, shape='conical'), tolerance=0.01)
run_test("H(Θ) Plane-Flow @ 30°", 1.18, get_H_function(30, shape='plane-flow'), tolerance=0.01)

# --- Test get_f_phi_i Function (Fig. 10.19) ---
print("\n## Testing f(phi_i) Function ##")
run_test("f(phi_i) @ 40°", 3.8, get_f_phi_i(40), tolerance=0.01)
run_test("f(phi_i) @ 50°", 6.0, get_f_phi_i(50), tolerance=0.01)

# --- Test get_flow_factor_ffp (Eq. 10.11) ---
print("\n## Testing ffp (Ratholing) Function ##")
# Test case 1: phi_e = 40, phi_lin = 40 -> f(phi_i) = 3.8
# ffp = (1+sin(40)) / (4*sin(40)) * 3.8 = (1.643 / 2.571) * 3.8 = 0.639 * 3.8 = 2.43
phi_lin_40 = get_phi_lin(40)
f_phi_i_40 = get_f_phi_i(phi_lin_40)
run_ffp_test("ffp @ phi_e=40, phi_lin=40", 2.43, get_flow_factor_ffp(40, phi_lin_40, f_phi_i_40), tolerance=0.1)

# Test case 2: phi_e = 30, phi_lin = 30 -> f(phi_i) = 2.4
# ffp = (1+sin(30)) / (4*sin(30)) * 2.4 = (1.5 / 2.0) * 2.4 = 0.75 * 2.4 = 1.8
phi_lin_30 = get_phi_lin(30)
f_phi_i_30 = get_f_phi_i(phi_lin_30)
run_ffp_test("ffp @ phi_e=30, phi_lin=30", 1.8, get_flow_factor_ffp(30, phi_lin_30, f_phi_i_30), tolerance=0.1)

# Test case 3: Check ffp >= 1.7 constraint
# phi_e = 60, phi_lin = 30 -> f(phi_i) = 2.4
# ffp = (1+sin(60)) / (4*sin(60)) * 2.4 = (1.866 / 3.464) * 2.4 = 0.539 * 2.4 = 1.29
# Should be floored at 1.7
run_ffp_test("ffp constraint @ phi_e=60, phi_lin=30", 1.7, get_flow_factor_ffp(60, phi_lin_30, f_phi_i_30), tolerance=0.01)


# --- Test Mass Flow Boundary Functions (Theta) ---
print("\n## Testing Mass Flow Boundaries (Theta) ##")
# Conical
run_test("Theta Conical @ phi_e=40, phi_x=20", 18.5, get_hopper_angle_theta(40, 20, 'conical'), tolerance=0.5) # 21.5 - 3 = 18.5
run_test("Theta Conical @ phi_e=50, phi_x=15", 18.0, get_hopper_angle_theta(50, 15, 'conical'), tolerance=0.5) # 21.0 - 3 = 18.0
run_test("Theta Conical @ phi_e=30, phi_x=25", 27.0, get_hopper_angle_theta(30, 25, 'conical'), tolerance=0.5) # 30.0 - 3 = 27.0
# Plane-Flow
run_test("Theta Plane-Flow @ phi_e=40, phi_x=20", 30.0, get_hopper_angle_theta(40, 20, 'plane-flow'), tolerance=0.5)
run_test("Theta Plane-Flow @ phi_e=50, phi_x=30", 19.0, get_hopper_angle_theta(50, 30, 'plane-flow'), tolerance=0.5)
run_test("Theta Plane-Flow @ phi_e=35, phi_x=10", 38.0, get_hopper_angle_theta(35, 10, 'plane-flow'), tolerance=0.5)

# --- Test Mass Flow Factor Functions (ff) ---
print("\n## Testing Flow Factor (ff) Interpolation ##")
# Conical
run_test("ff Conical @ phi_e=40, phi_x=20, theta=12.5", 1.4, get_flow_factor_ff(40, 20, 12.5, 'conical'), tolerance=0.1)
run_test("ff Conical @ phi_e=50, phi_x=15, theta=15.0", 1.4, get_flow_factor_ff(50, 15, 15.0, 'conical'), tolerance=0.1)
run_test("ff Conical @ phi_e=30, phi_x=25, theta=6.0", 1.4, get_flow_factor_ff(30, 25, 6.0, 'conical'), tolerance=0.1)
# Plane-Flow
run_test("ff Plane-Flow @ phi_e=40, phi_x=20, theta=21.0", 1.2, get_flow_factor_ff(40, 20, 21.0, 'plane-flow'), tolerance=0.1)
run_test("ff Plane-Flow @ phi_e=50, phi_x=30, theta=8.0", 1.2, get_flow_factor_ff(50, 30, 8.0, 'plane-flow'), tolerance=0.1)
run_test("ff Plane-Flow @ phi_e=60, phi_x=25, theta=11.0", 1.2, get_flow_factor_ff(60, 25, 11.0, 'plane-flow'), tolerance=0.1)

print("\n--- Test Run Complete ---")