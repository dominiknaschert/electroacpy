import electroacPy as ep
import numpy as np
import matplotlib.pyplot as plt

system = ep.load("AKT_Soundssystem_TOP_v1")
system.plot_results()

freq   = system.frequency

ev   = system.evaluation["AKT_interior"]
fp   = ev.setup["frf_interface"]
pMic = np.squeeze(fp.pMic).T  # (n_freq, n_mic) -> transpose zu (n_mic, n_freq)
xMic = fp.xMic                # (n_mic, 3)

n_mic, n_freq = pMic.shape

def spl(p):
    with np.errstate(divide="ignore"):
        return 20 * np.log10(np.abs(p) / 2e-5 / np.sqrt(2))

# Eindeutige xy-Positionen als Gruppen erkennen
xy = np.round(xMic[:, :2], 4)
unique_xy, group_idx = np.unique(xy, axis=0, return_inverse=True)
n_groups = len(unique_xy)
colors = plt.cm.tab10(np.linspace(0, 1, n_groups))

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle("Interior BEM — Frequenzgang Mikrofone", fontsize=13)

# --- links: alle Mikros einzeln, nach xy-Gruppe eingefärbt ---
ax = axes[0]
labeled = set()
for mic_idx in range(n_mic):
    g = group_idx[mic_idx]
    bx, by = unique_xy[g]
    label = f"({bx:.3f}, {by:.3f})" if g not in labeled else None
    labeled.add(g)
    ax.semilogx(freq, spl(pMic[mic_idx]), color=colors[g],
                alpha=0.5, linewidth=0.8, label=label)

ax.set_xlabel("Frequenz [Hz]")
ax.set_ylabel("SPL [dB]")
ax.set_title("Einzelne Mikrofone")
ax.legend(fontsize=7, loc="lower right")
ax.grid(True, which="both", alpha=0.3)
ax.set_xlim([freq[0], freq[-1]])

# --- rechts: Mittelwert je xy-Gruppe + Gesamtmittelwert ---
ax = axes[1]
group_means = []
for g, (bx, by) in enumerate(unique_xy):
    mask = group_idx == g
    mean_spl = spl(np.mean(pMic[mask], axis=0))
    group_means.append(mean_spl)
    ax.semilogx(freq, mean_spl, color=colors[g], linewidth=1.5,
                label=f"({bx:.3f}, {by:.3f})")

ax.semilogx(freq, np.mean(group_means, axis=0), "k--",
            linewidth=2, label="Gesamtmittel")

ax.set_xlabel("Frequenz [Hz]")
ax.set_title("Mittelwert je Basisposition")
ax.legend(fontsize=7, loc="lower right")
ax.grid(True, which="both", alpha=0.3)
ax.set_xlim([freq[0], freq[-1]])

plt.tight_layout()
plt.show()
