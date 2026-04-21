import electroacPy as ep

system = ep.load("KonAKT_Soundssystem_TOP_v2")

# system.plot_results(study="AKT_exterior", evaluation="spherical")

system.plot_results(study="AKT_exterior", evaluation="field_ext_xz")