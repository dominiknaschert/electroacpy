import electroacPy as ep
import numpy as np
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

frequency = np.arange(10, 10000, 1)
system = ep.loudspeakerSystem(frequency)

system.lem_driver("12NDL88", U, Le, Re, Cms, Mms, Rms, Bl, Sd)
system.lem_enclosure("12NDL88", 0.05, setDriver="12NDL88")

system.driver["12NDL88"].plotZe()
system.driver["12NDL88"].plotXVA()