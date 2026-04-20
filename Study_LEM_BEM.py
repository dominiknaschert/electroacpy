import electroacPy as ep
import numpy as np
import warnings

from mic_config import mic_positions, mic_labels

from study_config import RUN_INTERIOR, RUN_EXTERIOR

f_start = 20      # Startfrequenz (Hz)
f_end = 1000     # Endfrequenz (Hz)
bands_per_octave = 12

# Anzahl der Bänder
n_bands = int(np.floor(bands_per_octave * np.log2(f_end / f_start))) + 1

# Mit np.logspace die Mittenfrequenzen berechnen
frequency = f_start * 2 ** (np.arange(n_bands) / bands_per_octave)

print("Frequencies for LEM study:", frequency)
system = ep.loudspeakerSystem(frequency)

# Treiber-Parameter 12NDL88
fs = 51.0       # Hz
Re  = 5.0       # Ohm
Le  = 1.3e-3    # H
Bl  = 19.9        # T.m
Mms = 71e-3     # kg
Qms = 5.0
#Cms = 1/((2*np.pi*fs)**2*Mms)
#print("Cms:", Cms)
Cms = 137e-6    # m/N
#Qms = 5.0
#Rms = ((2*np.pi*fs*Mms)/Qms)
#print("Rms:", Rms)
Rms = 4.55     # kg/s
Sd  = 522e-4    # m^2
U = 2.83       # V (1W an 8 Ohm)

from electroacPy.acousticSim.bem import boundaryConditions

if RUN_INTERIOR:
    system.lem_driver("12NDL88", U, Le, Re, Cms, Mms, Rms, Bl, Sd, ref2bem=2)
    bc = boundaryConditions()
    bc.addSurfaceImpedance("interface_open", index=1,
                           data_type="absorption", value=1.0)
    system.study_acousticBEM("AKT_interior",
                             meshPath="mesh/AKT_Soundsystem_op1_v2.msh",
                             acoustic_radiator="12NDL88",
                             domain="interior",
                             boundary_conditions=bc)
    system.evaluation_pressureField(
        reference_study="AKT_interior",
        evaluation_name="field_ver",
        L1=0.5, L2=0.5, step=343/1000/6,
        plane="xz", offset=[0, 0, 0.2]
    )
    system.evaluation_pressureField(
        reference_study="AKT_interior",
        evaluation_name="field_hor",
        L1=0.5, L2=0.5, step=343/1000/6,
        plane="xy", offset=[0, 0, 0.2]
    )
    system.evaluation_fieldPoint(
        reference_study="AKT_interior",
        evaluation_name="frf_interface",
        microphonePositions=mic_positions,
    )

if RUN_EXTERIOR:
    system.lem_driver("12NDL88_ext", U, Le, Re, Cms, Mms, Rms, Bl, Sd, ref2bem=1)
    system.study_acousticBEM("AKT_exterior",
                             meshPath="mesh/AKT_Soundsystem_op1_exterior.msh",
                             acoustic_radiator="12NDL88_ext",
                             domain="exterior")
    system.evaluation_polarRadiation(
        reference_study="AKT_exterior",
        evaluation_name="polar_hor",
        min_angle=-180, max_angle=180, step=5,
        on_axis="y", direction="x",
        radius=2, offset=[0, 0, 0.2]
    )
    system.evaluation_polarRadiation(
        reference_study="AKT_exterior",
        evaluation_name="polar_ver",
        min_angle=-180, max_angle=180, step=5,
        on_axis="y", direction="z",
        radius=2, offset=[0, 0, 0.2]
    )
    system.evaluation_pressureField(
        reference_study="AKT_exterior",
        evaluation_name="field_ext_xz",
        L1=2, L2=2, step=343/1000/6,
        plane="xz", offset=[0, 0, 0.2]
    )

system.run()
system.plot_results()

ep.save("AKT_Soundssystem_TOP_v1", system)
