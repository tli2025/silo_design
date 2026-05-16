import math

from app_utils import (
    create_line_func,
    get_f_phi_i,
    get_flow_factor_ffp,
    find_positive_intersection,
)


def assert_close(test_name, expected, actual, tolerance=1e-6):
    error = abs(expected - actual)
    if error > tolerance:
        raise AssertionError(
            f"{test_name}: expected {expected}, got {actual}, error {error}"
        )
    print(f"PASS: {test_name}")


def test_create_line_func():
    func, (m, c) = create_line_func([0, 10], [1, 3])
    assert_close("create_line_func slope", 0.2, m)
    assert_close("create_line_func intercept", 1.0, c)
    assert_close("create_line_func value", 2.0, func(5))


def test_get_f_phi_i():
    assert_close("f(phi_i) at 40 deg", 3.55303, get_f_phi_i(40, show_message=False), tolerance=1e-5)
    assert_close("f(phi_i) at 50 deg", 5.05556, get_f_phi_i(50, show_message=False), tolerance=1e-5)


def test_get_flow_factor_ffp():
    f_phi_i_40 = get_f_phi_i(40, show_message=False)
    expected = ((1 + math.sin(math.radians(40))) / (4 * math.sin(math.radians(40)))) * f_phi_i_40
    assert_close(
        "ffp at phi_e=40, phi_lin=40",
        expected,
        get_flow_factor_ffp(40, 40, f_phi_i_40, show_message=False),
        tolerance=1e-6,
    )

    f_phi_i_30 = get_f_phi_i(30, show_message=False)
    assert_close(
        "ffp floor at low calculated value",
        1.7,
        get_flow_factor_ffp(60, 30, f_phi_i_30, show_message=False),
        tolerance=1e-6,
    )


def test_find_positive_intersection():
    root = find_positive_intersection(lambda x: 0.25 * x + 1, lambda x: x / 2, upper_hint=10)
    assert_close("positive intersection", 4.0, root)

    try:
        find_positive_intersection(lambda x: x + 1, lambda x: x + 2, upper_hint=10)
    except ValueError:
        print("PASS: no positive intersection raises ValueError")
    else:
        raise AssertionError("Expected ValueError when no positive intersection exists")


if __name__ == "__main__":
    test_create_line_func()
    test_get_f_phi_i()
    test_get_flow_factor_ffp()
    test_find_positive_intersection()
    print("All utility tests passed.")
