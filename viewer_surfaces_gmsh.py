import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
pfad = "mesh/AKT_Soundsystem_op1_v2.step"
pfad_2 = "mesh/Hifi Top_Dominik_v1_mit_horn.step"
# STEP- oder MSH-Datei laden
gmsh.open(pfad_2) 

gmsh.model.geo.synchronize()

# Alle Flächen (Dimension 2) holen
surfaces = gmsh.model.getEntities(dim=2)

for surf in surfaces:
    surf_id = surf[1]
    com = gmsh.model.occ.getCenterOfMass(2, surf_id)
    # Label mit Surface-ID anzeigen
    gmsh.model.occ.addPoint(*com, 0.0)
    gmsh.model.occ.synchronize()
    gmsh.model.addPhysicalGroup(0, [gmsh.model.occ.addPoint(*com, 0.0)], tag=surf_id)
    gmsh.model.setPhysicalName(0, surf_id, f"ID {surf_id}")

print("Alle Surface-IDs werden im Viewer als Punkte angezeigt.")
gmsh.fltk.run()
gmsh.finalize()