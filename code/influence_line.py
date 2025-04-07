# influence_line.py

import numpy as np
import matplotlib.pyplot as plt

class InfluenceLine1:
    def __init__(self, beam_length: float, num_points: int = 1000):
        self.L = beam_length
        self.n = num_points
        self.positions = np.linspace(0, self.L, self.n)

    def reaction_at_A(self):
        return (self.L - self.positions) / self.L

    def reaction_at_B(self):
        return self.positions / self.L

    def shear_force(self, p: float):
        IL_SF = np.zeros_like(self.positions)
        for i, x in enumerate(self.positions):
            if x < p:
                IL_SF[i] = (self.L - p) / self.L
            elif x > p:
                IL_SF[i] = -p / self.L
            else:
                IL_SF[i] = np.nan  # Discontinuity at x = p
        return IL_SF

    def max_shear_force(self, W1, W2, x):
        """
        Return SF envelope (list of (position, SF)), max SF value, and its position.
        """
        max_sf = float('-inf')
        max_sf_pos = 0.0
        sf_envelope = []
        step = 0.01
        a = 0.0

        while a + x <= self.L:
            loads = [(a, W1), (a + x, W2)]
            moment_sum = sum([pos * w for pos, w in loads])
            total_load = W1 + W2
            R_B = moment_sum / self.L
            R_A = total_load - R_B
            for p in [i * step for i in range(int(self.L / step) + 1)]:
                sf = R_A
                for pos, w in loads:
                    if pos < p:
                        sf -= w
                sf_envelope.append((p, sf))
                if abs(sf) > abs(max_sf):
                    max_sf = sf
                max_sf_pos = p
                a += step
            
        return sf_envelope, round(max_sf, 3), round(max_sf_pos, 3)
    
    
    def max_bending_moment(self, W1, W2, x):
       """
       Return BM envelope (list of (position, BM)), max BM value, and its position.
       """
       max_bm = float('-inf')
       max_bm_pos = 0.0
       bm_envelope = []
       step = 0.01
       a = 0.0

       while a + x <= self.L:
        loads = [(a, W1), (a + x, W2)]
        moment_sum = sum([pos * w for pos, w in loads])
        total_load = W1 + W2
        R_B = moment_sum / self.L
        R_A = total_load - R_B

        for p in [i * step for i in range(int(self.L / step) + 1)]:
            bm = R_A * p  # Initial moment by RA
            for pos, w in loads:
                if pos <= p:
                    bm -= w * (p - pos)
            bm_envelope.append((p, bm))
            if abs(bm) > abs(max_bm):
                max_bm = bm
                max_bm_pos = p

        a += step
        return bm_envelope, round(max_bm, 3), round(max_bm_pos, 3)
    
    def apply_loads(self, IL: np.ndarray, loads: list):
        total_effect = 0.0
        for W, pos in loads:
            idx = np.argmin(np.abs(self.positions - pos))
            total_effect += W * IL[idx]
        return total_effect

    def plot_influence_line(self, IL: np.ndarray, title: str):
        plt.figure(figsize=(10, 4))
        plt.plot(self.positions, IL, label=title)
        plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
        plt.title(f"Influence Line for {title}")
        plt.xlabel("Beam Length")
        plt.ylabel("Influence Value")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

class InfluenceLine:
    def __init__(self, length):
        self.length = length

    def reaction_at_A(self, W1, W2, x):
        """
        Calculate the maximum reaction at support A using influence line for two-point moving load.
        Assumes loads W1 and W2 spaced by x.
        """
        L = self.length
        max_RA = 0
        step = 0.01

        pos = 0.0
        while pos + x <= L:
            # W1 at pos, W2 at pos + x
            a = pos
            b = pos + x
            RA = W1 * (L - a) / L + W2 * (L - b) / L
            max_RA = max(max_RA, RA)
            pos += step

        return max_RA

    def reaction_at_B(self, W1, W2, x):
        """
        Calculate the maximum reaction at support B using influence line for two-point moving load.
        Assumes loads W1 and W2 spaced by x.
        """
        L = self.length
        max_RB = 0
        step = 0.01

        pos = 0.0
        while pos + x <= L:
            # W1 at pos, W2 at pos + x
            a = pos
            b = pos + x
            RB = W1 * a / L + W2 * b / L
            max_RB = max(max_RB, RB)
            pos += step

        return max_RB

# Example usage
if __name__ == "__main__":
    beam = InfluenceLine1(beam_length=10.0)

    IL_RA = beam.reaction_at_A()
    IL_RB = beam.reaction_at_B()
    IL_SF = beam.shear_force(p=5.0)
    IL_BM = beam.bending_moment(p=5.0)

    beam.plot_influence_line(IL_RA, "Reaction at A")
    beam.plot_influence_line(IL_RB, "Reaction at B")
    beam.plot_influence_line(IL_SF, "Shear Force at p = 5.0")
    beam.plot_influence_line(IL_BM, "Bending Moment at p = 5.0")
