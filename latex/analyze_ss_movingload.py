"""
Main analysis module: analyze_ss_movingload.py
Performs moving load analysis on a simply supported beam using hybrid approach
(beam calculation + influence lines + visualization)
"""

from beam_calculator import Beam
from influence_line import InfluenceLine1 , InfluenceLine
from visualization import Visualization

def analyze_beam(L, W1, W2, x):
    """
    Analyze a simply supported beam under two moving point loads using influence lines and direct analysis.

    Parameters:
        L (float): Length of the beam in meters (L > 0)
        W1 (float): Magnitude of first moving load in kN (W1 > 0)
        W2 (float): Magnitude of second moving load in kN (W2 > 0)
        x (float): Spacing between W1 and W2 (0 < x < L)

    Returns:
        dict: Contains results including max reactions, shear force, bending moment, envelopes, and critical positions
    """

    # Input Validation
    if L <= 0:
        raise ValueError("Beam length must be positive.")
    if W1 <= 0 or W2 <= 0:
        raise ValueError("Loads must be positive.")
    if x <= 0 or x >= L:
        raise ValueError("Spacing x must be positive and less than beam length.")

    # Setup
    beam = Beam(L)
    infl = InfluenceLine1(L)
    infl2 = InfluenceLine(L)
    viz = Visualization(L)

    # Initialize result storage
    results = {}

    # Maximum Reactions
    max_RA = infl2.reaction_at_A(W1, W2, x)
    max_RB = infl2.reaction_at_B(W1, W2, x)
    results['Max Reaction at A'] = round(max_RA, 3)
    results['Max Reaction at B'] = round(max_RB, 3)

    # Specific Bending Moment when W1 is at 0 and W2 at x
    loads = [(0, W1), (x, W2)]
    # W1 at 0.0 and W2 at x
    # Specific Point Analysis: BM_01 (when W1 at 0.0 and W2 at x)
    # Specific Point Analysis: BM_01 (when W1 at 0.0 and W2 at x)
    BM_01_position = (0.0 * W1 + x * W2) / (W1 + W2)  # effective position of combined load
    BM_01 = beam.bending_moment_two(W1, 0.0, W2, x, BM_01_position)

    results['BM when W1 at 0'] = round(BM_01, 3)

    # Shear Force at midspan for critical position
    midspan = L / 2
    SF_mid = beam.shear_force_at(loads, midspan)
    results['Shear Force at 0.5L'] = round(SF_mid, 3)

    # Maximum Effects via influence line
    sf_envelope, sf_max_val, sf_max_pos = infl.max_shear_force(W1, W2, x)
    bm_envelope, bm_max_val, bm_max_pos = infl.max_bending_moment(W1, W2, x)

    results['Max SF'] = round(sf_max_val, 3)
    results['SF Location from A'] = round(sf_max_pos, 3)
    results['Max BM'] = round(bm_max_val, 3)
    results['BM Location from A'] = round(bm_max_pos, 3)

    # Visualization
    viz.plot_beam_with_loads(loads)
    viz.plot_shear_force_envelope(sf_envelope)
    viz.plot_bending_moment_envelope(bm_envelope)

    return results


# Example usage (remove or comment during deployment)
if __name__ == "__main__":
    result = analyze_beam(L=10.0, W1=5.0, W2=10.0, x=2.0)
    for key, val in result.items():
        print(f"{key}: {val}")
