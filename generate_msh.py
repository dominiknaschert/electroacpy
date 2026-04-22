import electroacPy as ep
from study_config import RUN_INTERIOR, RUN_EXTERIOR

lmax = 343 / 1e3 / 6
lmin = lmax / 10
pfad = "mesh/AKT_Soundsystem_op1_v2.step"
pfad_2 = "mesh/Hifi Top_Dominik_v1_mit_horn.step"
ext = "mesh_KontAKT/Hifi_Top_Dominik_v1_exterior.step" 
int = "mesh_KontAKT/Hifi_Top_Dominik_v1_interior.step"

if RUN_INTERIOR:
    cad = ep.gtb.meshCAD(int, minSize=lmin, maxSize=lmax)
    cad.addSurfaceGroup("interface", [18],                                                   groupNumber=1)
    cad.addSurfaceGroup("treiber",   [17],                                                   groupNumber=2)
    cad.addSurfaceGroup("gehaeuse",  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], groupNumber=3)
    cad.mesh("mesh_KontAKT/Hifi_Top_Dominik_v1_interior", order=2)
    print("Interior Mesh erzeugt: mesh_KontAKT/Hifi_Top_Dominik_v1_interior.msh")

# Treiber oben ist 90 treiber unten ist 88
if RUN_EXTERIOR:
    cad_ext = ep.gtb.meshCAD(ext, minSize=lmin, maxSize=lmax)
    cad_ext.addSurfaceGroup("treiber", [86, 87], groupNumber=1)
    cad_ext.addSurfaceGroup("gehaeuse", [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
        43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
        83, 84, 85, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
    ], groupNumber=2)
    cad_ext.mesh("mesh_KontAKT/Hifi_Top_Dominik_v1_exterior", order=2)
    print("Exterior Mesh erzeugt: mesh_KontAKT/Hifi_Top_Dominik_v1_exterior.msh")
