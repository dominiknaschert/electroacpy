import numpy as np

# 4 Basispositionen (x, y) — im Viewer anpassen
base_positions = [
    (0.02,  0.02),   # links
    (0.065, 0.14),   # mitte-links
    (0.2,   0.025),   # mitte
    (0.07,  0.08),   # rechts
    (0.28,  0.02),   # weit rechts
    (0.13,  0.08),   # mitte-rechts
    (0.10,  0.03),   # links-tief
]

# z-Raster: von z_min bis z_max mit n_z Punkten
z_min = 0.060
z_max = 0.370
n_z   = 5

z_vals = np.linspace(z_min, z_max, n_z)

mic_positions = np.array([
    [x, y, z]
    for (x, y) in base_positions
    for z in z_vals
])

mic_labels = [f"({x:.2f},{y:.2f}) z={z:.2f}"
              for (x, y) in base_positions
              for z in z_vals]
