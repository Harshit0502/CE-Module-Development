
---

## 📌 How It Works

1. **Define beam length `L` and two point loads (`W1`, `W2`)** with distance `x` between them.
2. **Move the pair of loads** from start to end of the beam.
3. At each position:
   - Compute reactions at supports A and B
   - Calculate Shear Force and Bending Moment at every section
   - Track the **maximum value** and its location
4. Visualize everything: beam, loads, and diagrams.

---

## 📊 Visualization

### 🔹 Beam with Loads
- Shows the beam with pin and roller supports
- Arrows denote the position and magnitude of loads

### 🔸 Shear Force Envelope
- Shear force variation as the loads move
- Highlights peak shear and its location

### 🔹 Bending Moment Envelope
- Bending moment variation across the beam
- Shows max moment and where it occurs

---

## ▶️ Example

```python
from analyze_ss_movingload import analyze_beam
from visualization import Visualization

# Inputs
L = 10.0     # Beam Length
W1 = 5.0     # Load 1 (kN)
W2 = 10.0    # Load 2 (kN)
x = 2.0      # Distance between loads (m)

# Analysis
sf_env, sf_max_val, sf_max_pos, bm_env, bm_max_val, bm_max_pos = analyze_beam(L, W1, W2, x)

# Visualization
viz = Visualization(L)
viz.plot_shear_force_envelope(sf_env)
viz.plot_bending_moment_envelope(bm_env)
