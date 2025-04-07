import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np



# Visualization class for a simply supported beam with moving loads
# This class is responsible for drawing the beam, supports, loads, and diagrams.

# It uses matplotlib for rendering the graphics.
# The class is designed to be reusable and modular, allowing for easy updates and modifications.


class Visualization:
    def __init__(self, length):
        self.length = length
        self.fig, self.ax = plt.subplots(figsize=(12, 2))
        self.ax.set_xlim(-0.1 * length, 1.1 * length)
        self.ax.set_ylim(-2, 2)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.supports_drawn = False

    def draw_beam(self):
        self.ax.plot([0, self.length], [0, 0], 'k', linewidth=4)
        self.ax.text(self.length/2, 0.2, f"Beam (L = {self.length})", ha='center', fontsize=10)

    def draw_supports(self):
        # Pin support at A (triangle)
        triangle = patches.Polygon([[0, 0], [-0.3, -0.5], [0.3, -0.5]], color='black')
        self.ax.add_patch(triangle)
        # Roller support at B (circle)
        circle = patches.Circle((self.length, -0.5), 0.15, color='black')
        self.ax.add_patch(circle)
        self.supports_drawn = True

    def draw_point_load(self, position, magnitude, label=None):
        self.ax.arrow(position, 0.5, 0, -0.5, head_width=0.1, head_length=0.2, fc='red', ec='red')
        self.ax.text(position, 0.6, f"{label or magnitude}kN", ha='center', color='red', fontsize=9)

    def plot_beam_with_loads(self, loads):
        self.clear()
        self.__init__(self.length)
        self.draw_beam()
        self.draw_supports()
        for pos, mag in loads:
            self.draw_point_load(pos, mag)
        self.show()

    def plot_shear_force_envelope(self, sf_envelope):
        positions, shear_forces = zip(*sf_envelope)
        plt.figure(figsize=(12, 4))
        plt.plot(positions, shear_forces, label="Shear Force Envelope", color='blue')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel("Position along Beam (m)")
        plt.ylabel("Shear Force (kN)")
        plt.title("Shear Force Envelope")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_bending_moment_envelope(self, bm_envelope):
        positions, moments = zip(*bm_envelope)
        plt.figure(figsize=(12, 4))
        plt.plot(positions, moments, label="Bending Moment Envelope", color='green')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel("Position along Beam (m)")
        plt.ylabel("Bending Moment (kNm)")
        plt.title("Bending Moment Envelope")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


    def show(self):
        if not self.supports_drawn:
            self.draw_supports()
        plt.show()

    def clear(self):
        plt.clf()
