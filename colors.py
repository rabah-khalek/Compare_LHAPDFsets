import sys
import numpy as np
import yaml
import matplotlib.pyplot as py
from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)

InputCard = sys.argv[1]
outputname = InputCard.split(".yaml")[0]
Fits_catalog = None
with open(InputCard) as f:
    Fits_catalog = yaml.safe_load(f)

Type_of_sets = ["PDFs", "nPDFs", "FFs"]

fig, (ax0, ax1, ax2) = py.subplots(nrows=3)
axs = [ax0, ax1, ax2]
colors={}
for Type_of_set in Type_of_sets:
    if Fits_catalog['Global Settings'][Type_of_set]["colors"] == "default":
        colors[Type_of_set] = py.rcParams['axes.prop_cycle'].by_key()['color']
    else:
        colors[Type_of_set] = Fits_catalog['Global Settings'][Type_of_set]["colors"]

x = np.linspace(0, 2 * np.pi, 50)
offsets = np.linspace(0, 2 * np.pi, 4, endpoint=False)
yy = np.transpose([np.sin(x + phi) for phi in offsets])

for iset, Type_of_set in enumerate(Type_of_sets):
    # +cycler(linestyle=['-', '-', '-', '-']))
    cycl = (py.cycler(color=colors[Type_of_set]))

    py.rc('lines', linewidth=4)
    py.rc('axes', prop_cycle=cycl)

    if Type_of_set == "FFs":
        dist = "$zD^{h}_{q}$"
    elif Type_of_set == "PDFs":
        dist = "$xf^{p}_{q}$"
    elif Type_of_set == "nPDFs":
        dist = "$xf^{A}_{q}$"

    axs[iset].set_prop_cycle(cycl)
    axs[iset].plot(yy)
    axs[iset].set_title(r'{\rm '+Type_of_set+' ('+dist+')}')

    axs[iset].set_xticklabels([])
    axs[iset].set_yticklabels([])
    axs[iset].tick_params(which='major', length=0)
    axs[iset].tick_params(which='minor', length=0)

    # Add a bit more space between the two plots.
    fig.subplots_adjust(hspace=0.3)

py.tight_layout()
py.savefig("colors.png")
py.savefig("colors.pdf")
