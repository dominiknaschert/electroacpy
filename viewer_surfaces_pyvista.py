import pyvista as pv
import numpy as np
import gmsh
from mic_config import mic_positions, mic_labels

mic_treiber = np.array([
    [-0.1967,  0.2879, -0.0783],  # vor treiber_rechts
    [ 0.1967,  0.2879, -0.0783],  # vor treiber_links
])
mic_treiber_labels = ["Test: treiber_rechts", "Test: treiber_links"]
pfad = "mesh/AKT_Soundsystem_op1_exterior.msh"
int = "mesh_KontAKT/Hifi_Top_Dominik_v1_interior.msh"
ext = "mesh_KontAKT/Hifi_Top_Dominik_v1_exterior.msh"
INTERIOR_OFFSET = np.array([0.0, 0.0, 0.0])

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
gmsh.open(ext)

node_tags, coords, _ = gmsh.model.mesh.getNodes()
points = coords.reshape(-1, 3)
node_index = {tag: i for i, tag in enumerate(node_tags)}

all_tris = []
all_phys = []
pg_names = {}

for dim, pg_tag in gmsh.model.getPhysicalGroups(dim=2):
    name = gmsh.model.getPhysicalName(dim, pg_tag)
    pg_names[pg_tag] = name
    for surf_tag in gmsh.model.getEntitiesForPhysicalGroup(dim, pg_tag):
        elem_types, elem_tags, elem_nodes = gmsh.model.mesh.getElements(dim=2, tag=surf_tag)
        for etype, etags, enodes in zip(elem_types, elem_tags, elem_nodes):
            if etype == 2:
                tris = enodes.reshape(-1, 3)
                for tri in tris:
                    all_tris.append([node_index[n] for n in tri])
                    all_phys.append(pg_tag)

gmsh.finalize()

all_tris = np.array(all_tris)
all_phys = np.array(all_phys)

faces = np.hstack([np.full((len(all_tris), 1), 3), all_tris])
surf = pv.PolyData(points, faces)
surf["phys_id"] = all_phys

# Mikrofon-Punkte leicht nach innen verschoben
mic_points_offset = mic_positions + INTERIOR_OFFSET
mic_cloud = pv.PolyData(mic_points_offset)

plotter = pv.Plotter()
plotter.add_axes(xlabel="X", ylabel="Y", zlabel="Z")

# Koordinatensystem in der Mitte des Meshes
center = np.array(surf.center)
axis_len = surf.length * 0.2
for vec, color, label in [
    ([1, 0, 0], "red",   "X"),
    ([0, 1, 0], "green", "Y"),
    ([0, 0, 1], "blue",  "Z"),
]:
    tip = center + axis_len * np.array(vec)
    arrow = pv.Arrow(start=center, direction=vec, scale=axis_len,
                     tip_length=0.25, tip_radius=0.05, shaft_radius=0.02)
    plotter.add_mesh(arrow, color=color)
    plotter.add_point_labels(pv.PolyData(tip.reshape(1, 3)), [label],
                             font_size=14, text_color=color,
                             point_size=0, always_visible=True, shape=None)

# Farben pro Physical Group: Treiber leuchtend, Rest grau/gedämpft
GROUP_COLORS = {
    "treiber":       "#FF2200",
    "treiber_oben":  "#FF8800",
    "treiber_unten": "#FFCC00",
    "gehaeuse":      "#888888",
    "enclosure":     "#555555",
}
DEFAULT_COLOR = "#999999"

unique_tags = np.unique(all_phys)
for tag in unique_tags:
    name = pg_names.get(tag, str(tag))
    color = GROUP_COLORS.get(name, DEFAULT_COLOR)
    mask = all_phys == tag
    tri_indices = np.where(mask)[0]
    sub_faces = np.hstack([np.full((len(tri_indices), 1), 3), all_tris[tri_indices]])
    sub_mesh = pv.PolyData(points, sub_faces)
    opacity = 0.95 if "treiber" in name else 0.55
    plotter.add_mesh(sub_mesh, show_edges=True, color=color,
                     opacity=opacity, label=f"{tag}: {name}")

plotter.add_legend(bcolor="white", border=True)

# Mikros als Kugeln + Labels
for i, (pos, label) in enumerate(zip(mic_points_offset, mic_labels)):
    sphere = pv.Sphere(radius=0.008, center=pos)
    plotter.add_mesh(sphere, color="cyan")
    plotter.add_point_labels(pv.PolyData(pos.reshape(1, 3)),
                             [f"Mic {i+1}: {label}"],
                             font_size=12, text_color="cyan",
                             point_color="cyan", point_size=0,
                             always_visible=True, shape=None)

# Test-Mics vor den Treibern (gelbe Würfel)
for pos, label in zip(mic_treiber, mic_treiber_labels):
    cube = pv.Cube(center=pos, x_length=0.015, y_length=0.015, z_length=0.015)
    plotter.add_mesh(cube, color="yellow")
    plotter.add_point_labels(pv.PolyData(pos.reshape(1, 3)), [label],
                             font_size=13, text_color="yellow",
                             point_size=0, always_visible=True, shape=None)

plotter.add_text("Surface Physical Groups + Mikrofon-Positionen", font_size=14)
plotter.show()
