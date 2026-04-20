import electroacPy as ep
from study_config import RUN_INTERIOR, RUN_EXTERIOR

lmax = 343 / 1e3 / 6
lmin = lmax / 10

if RUN_INTERIOR:
    cad = ep.gtb.meshCAD("mesh/AKT_Soundsystem_op1_v2.step", minSize=lmin, maxSize=lmax)
    cad.addSurfaceGroup("interface", [18],                                                   groupNumber=1)
    cad.addSurfaceGroup("treiber",   [17],                                                   groupNumber=2)
    cad.addSurfaceGroup("gehaeuse",  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], groupNumber=3)
    cad.mesh("mesh/AKT_Soundsystem_op1_v2", order=2)
    print("Interior Mesh erzeugt: mesh/AKT_Soundsystem_op1_v2.msh")

if RUN_EXTERIOR:
    cad_ext = ep.gtb.meshCAD("mesh/AKT_Soundsystem_op1_extirior.step", minSize=lmin, maxSize=lmax)
    cad_ext.addSurfaceGroup("treiber",  [8],                                                    groupNumber=1)
    cad_ext.addSurfaceGroup("gehaeuse", [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16], groupNumber=2)
    cad_ext.mesh("mesh/AKT_Soundsystem_op1_exterior", order=2)
    print("Exterior Mesh erzeugt: mesh/AKT_Soundsystem_op1_exterior.msh")
