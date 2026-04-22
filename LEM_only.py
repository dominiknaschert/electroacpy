import electroacPy as ep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
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

Liter = 108.9 # Rückkammer des Gehäuses in Litern
Volumen = Liter/1000 # in m³

frequency = np.arange(10, 10000, 1)



sys_free = ep.loudspeakerSystem(frequency)
sys_free.lem_driver("12NDL88", U, Le, Re, Cms, Mms, Rms, Bl, Sd)

# Impedanz-Plot (nur Treiber)
sys_free.driver["12NDL88"].plotZe()

# --- Geschlossenes Gehäuse (sealed, Vb = 108.9 Liter) ---
sys_box = ep.loudspeakerSystem(frequency)
sys_box.lem_driver("12NDL88", U, Le, Re, Cms, Mms, Rms, Bl, Sd)
sys_box.lem_enclosure("12NDL88", Volumen, setDriver="12NDL88")


# XVA-Vergleich: Freiluft vs. Gehäuse
drv = sys_free.driver["12NDL88"]
enc = sys_box.enclosure["12NDL88"]
f   = drv.f_array
s   = 1j * 2 * np.pi * f

x_free = drv.Hx * 1e3
v_free = drv.Hv
a_free = drv.Ha

x_box  = enc.v / s * 1e3
v_box  = enc.v
a_box  = enc.v * s

fig, ax = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
ax[0].semilogx(f, np.abs(x_free), label="Freiluft")
ax[0].semilogx(f, np.abs(x_box),  label=f"Sealed {Liter} L")
ax[1].semilogx(f, np.abs(v_free), label="Freiluft")
ax[1].semilogx(f, np.abs(v_box),  label=f"Sealed {Liter} L")
ax[2].semilogx(f, np.abs(a_free), label="Freiluft")
ax[2].semilogx(f, np.abs(a_box),  label=f"Sealed {Liter} L")
ax[0].set(ylabel="mm",   title="Auslenkung")
ax[1].set(ylabel="m/s",  title="Geschwindigkeit")
ax[2].set(ylabel="m/s²", title="Beschleunigung", xlabel="Frequenz [Hz]")
for a in ax:
    a.grid(which="both", linestyle="dotted")
    a.legend()
plt.tight_layout()
plt.show()

# SPL @ 1m
c   = enc.c
rho = enc.rho
k   = 2 * np.pi * f / c

p_free = 1j * k * rho * c * drv.Q * np.exp(-1j * k) / (2 * np.pi)
p_box  = 1j * k * rho * c * enc.Q * np.exp(-1j * k) / (2 * np.pi)

spl_free = 20 * np.log10(np.abs(p_free) / 20e-6)
spl_box  = 20 * np.log10(np.abs(p_box)  / 20e-6)

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.semilogx(f, spl_free, label="Freiluft")
ax2.semilogx(f, spl_box,  label=f"Sealed {Liter} L")
ax2.set(xlabel="Frequenz [Hz]", ylabel="SPL [dB]", title="SPL @ 1m")
ax2.grid(which="both", linestyle="dotted")
ax2.legend()
plt.tight_layout()
plt.show()
