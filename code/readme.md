---

## 📌 How It Works

**code_definitions**:
  analyze_ss_movingload.py:
    analyze_beam:
      description: >
        Orchestrates the full analysis. Initializes influence line object,
        computes shear force and bending moment envelopes, and returns max values.

---

 ## 📌 influence_line.py:

   ** InfluenceLine1**:
      description: Initializes the influence line model for a simply supported beam.
      methods:
        reaction_at_A: Returns influence line values for reaction at support A.
        reaction_at_B: Returns influence line values for reaction at support B.
        shear_force:
          params: p (float)
          description: Computes shear force influence line at section p.
        max_shear_force:
          params: W1 (float), W2 (float), x (float)
          description: >
            Slides two loads across the beam to compute shear force envelope,
            maximum SF value, and its position.
        bending_moment:
          params: p (float)
          description: Returns bending moment influence line at section p.
        max_bending_moment:
          params: W1 (float), W2 (float), x (float)
          description: >
            Slides two loads across the beam to compute bending moment envelope,
            maximum BM value, and its position.
        apply_loads:
          params: IL (ndarray), loads (list)
          description: Calculates total effect of loads using the influence line.
        plot_influence_line:
          params: IL (ndarray), title (str)
          description: Plots the influence line diagram with appropriate labels.

---

## 📌 visualization.py:
    
   **Visualization:**
      description: Initializes the beam visualization canvas with supports and scaling.
      methods:
        draw_beam: Draws the beam line.
        draw_supports: Draws supports at beam ends (pin and roller).
        draw_point_load:
          params: position (float), magnitude (float), label (str, optional)
          description: Draws red arrow representing a point load.
        plot_beam_with_loads:
          params: loads (list of tuples)
          description: Plots the beam with applied loads.
        plot_shear_force_envelope:
          params: sf_envelope (list of tuples)
          description: Plots shear force envelope along the beam.
        plot_bending_moment_envelope:
          params: bm_envelope (list of tuples)
          description: Plots bending moment envelope for the beam.
