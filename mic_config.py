import numpy as np

# Interface liegt bei y=0, x=-0.385..0.385, z=-0.400..-0.385
# Mics 5cm vor dem Interface (y=-0.05), symmetrisches x-Raster, z in Interface-Mitte

spacing  = 0.10   # gleichmäßiger Abstand in x und y
x_offset = 0.0    # Verschiebung des Rasters in x
y_offset = 0.52    # Verschiebung des Rasters in y

x_vals = np.arange(-0.30, 0.31, spacing) + x_offset
y_vals = -np.arange(spacing, 4*spacing + 0.001, spacing) + y_offset
z_mic  = -0.02  # Mitte der Interface-Fläche

mic_positions = np.array([
    [x, y, z_mic]
    for y in y_vals
    for x in x_vals
])

mic_labels = [f"({x:.2f}, y={y:.2f})" for y in y_vals for x in x_vals]
