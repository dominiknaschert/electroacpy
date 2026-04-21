import pyvista as pv
import numpy as np
import gmsh
from mic_config import mic_positions, mic_labels
pfad = "mesh/AKT_Soundsystem_op1_exterior.msh"

INTERIOR_OFFSET = np.array([0.0, 0.0, 0.0])

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
gmsh.open(pfad)

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
plotter.add_mesh(surf, show_edges=True, scalars="phys_id", cmap="tab10",
                 show_scalar_bar=True, opacity=0.6)

# Mikros als Kugeln + Labels
for i, (pos, label) in enumerate(zip(mic_points_offset, mic_labels)):
    sphere = pv.Sphere(radius=0.008, center=pos)
    plotter.add_mesh(sphere, color="red")
    plotter.add_point_labels(pv.PolyData(pos.reshape(1, 3)),
                             [f"Mic {i+1}: {label}"],
                             font_size=12, text_color="red",
                             point_color="red", point_size=0,
                             always_visible=True, shape=None)

# Legende Physical Groups
legend = [[f"{tag}: {name}", "tab10"] for tag, name in pg_names.items()]
plotter.add_text("Surface Physical Groups + Mikrofon-Positionen", font_size=14)
plotter.show()
