#-- Author: Rabah Abdul Khalek <rabah.khalek@gmail.com>
import src.sets as SETS
import matplotlib.gridspec as gridspec
import warnings
import matplotlib.ticker
import sys
import os
#os.environ["LHAPDF_DATA_PATH"] = "/Users/rabah/Documents/FF_SIDIS_project/FF_SIDIS_Files/Fits/MAPFF20/Q2_00/MAPFF20_PI_NLO_Q2_00\
#                                 :/Users/rabah/Documents/FF_SIDIS_project/FF_SIDIS_Files/Fits/MAPFF20/Q2_00/MAPFF20_PI_NNLO_Q2_00\
#                                 :/Users/rabah/Documents/FF_SIDIS_project/FF_SIDIS_Files/Fits/MAPFF20/Q2_00/MAPFF20_KA_NLO_Q2_00\
#                                 :/Users/rabah/Documents/FF_SIDIS_project/FF_SIDIS_Files/Fits/MAPFF20/Q2_00/MAPFF20_KA_NNLO_Q2_00"

import numpy as np
import yaml
import matplotlib.pyplot as py
from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
warnings.filterwarnings("ignore")

Ratio_den_Set = 0  # 0 for the first PDF to be chosen as denominator in the ratio

N1s = ["_p", "_N1", "CT14nlo", "nCTEQ15WZSIH_1_1"]

#---- plotting settings

colors = {}
lss = {}

InputCard = sys.argv[1]
outputname = InputCard.split(".yaml")[0]+"_statconv"
Fits_catalog = None
with open(InputCard) as f:
    Fits_catalog = yaml.safe_load(f)

comparison_choices = Fits_catalog['Global Settings']["plot"]

fontsize = Fits_catalog['Global Settings']["fontsize"]
legend_fontsize = Fits_catalog['Global Settings']["legend_fontsize"]
fontsize_scaling = 0.25*(1.-20./fontsize)
output_format = Fits_catalog['Global Settings']["output_format"]
rc('xtick', labelsize=fontsize)
rc('ytick', labelsize=fontsize)

if comparison_choices == "all":
    comparison_choices = list(Fits_catalog.keys())

if 'Global Settings' in comparison_choices:
    comparison_choices.remove("Global Settings")

for comparison_choice in comparison_choices:
    print("\n---"+comparison_choice+"---")

    Setsnames = Fits_catalog[comparison_choice]["Setsnames"]
    Setlabels = Fits_catalog[comparison_choice]["Setlabels"]
    Error_type = Fits_catalog[comparison_choice]["Error_type"]
    Nreps = Fits_catalog[comparison_choice]["Nreps"]
    flavors_to_plot = Fits_catalog[comparison_choice]["flavors_to_plot"]
    Comparisons = Fits_catalog[comparison_choice]["Comparisons"]
    Type_of_sets = Fits_catalog[comparison_choice]["Type_of_sets"]
    if "nucleus" in Fits_catalog[comparison_choice].keys():
        NUCLEUS = Fits_catalog[comparison_choice]["nucleus"]
    else:
        NUCLEUS = ""
    if "uncertainty" in Fits_catalog[comparison_choice].keys():
        UNCERTAINTY = Fits_catalog[comparison_choice]["uncertainty"]
    else:
        UNCERTAINTY = "68CL"
    PTO = Fits_catalog[comparison_choice]["PTO"]
    PTO = Fits_catalog[comparison_choice]["PTO"]
    hadron = " "
    if "hadron" in Fits_catalog[comparison_choice].keys():
        hadron = Fits_catalog[comparison_choice]["hadron"]

    if Fits_catalog['Global Settings'][Type_of_sets]["colors"] == "default":
        colors[Type_of_sets] = py.rcParams['axes.prop_cycle'].by_key()['color']
    else:
        colors[Type_of_sets] = Fits_catalog['Global Settings'][Type_of_sets]["colors"]

    if "colors" in Fits_catalog[comparison_choice].keys():
        colors[Type_of_sets] = Fits_catalog[comparison_choice]["colors"]

    if "lss" in Fits_catalog[comparison_choice].keys():
        lss[Type_of_sets] = Fits_catalog[comparison_choice]["lss"]

    if not os.path.isdir(outputname):
        os.system('mkdir '+outputname)

    Q = Fits_catalog[comparison_choice]["Q"]
    Q2 = Q**2

    #xmin, xmax, nx = Fits_catalog[comparison_choice]["x"][0], Fits_catalog[
    #    comparison_choice]["x"][1], Fits_catalog[comparison_choice]["x"][2]

    X_values=np.array([0.01,0.1])
    

    for ixx, X_value in enumerate(X_values):

        Sets = {}
        neutron_Sets = {}
        nonuclear_Sets = {}
        LHAPDFSets = {}
        neutron_LHAPDFSets = {}
        Y_pull = {}
        Y_rel = {}
        Nset = 0

        print("(x="+str(X_value)+")")
        X_value=np.array([X_value])

        for iSet, Setname in enumerate(Setsnames):
            print("Loading "+Setname+"")

            Nreps[iSet] =min(Nreps)
            
            if not Setname in LHAPDFSets.keys():
                Sets[Setname] = SETS.Get(Setname, X_value, Q, Nreps[iSet]+1)
                LHAPDFSets[Setname] = SETS.GetStats(
                    Sets[Setname], Error_type[iSet])

                if "NuclearRatio" in Comparisons.keys():
                    neutron_Sets[Setname] = SETS.Get(
                        Setname, X_value, Q, Nreps[iSet]+1, True)
                    #nonuclear_Sets[Setname] = {}
                    neutron_LHAPDFSets[Setname] = SETS.GetStats(
                        neutron_Sets[Setname], Error_type[iSet])

                if "NuclearRatio_pull" in Comparisons.keys() and (not any(ext in Setname for ext in N1s) or Setname == "EPPS16nlo_CT14nlo_Pb208"):
                    Y_pull[Setname] = {}

                if "NuclearRatio_RelativeUncertainty" in Comparisons.keys() and (not any(ext in Setname for ext in N1s) or Setname == "EPPS16nlo_CT14nlo_Pb208"):
                    Y_rel[Setname] = {}
            Nset += 1

        print("Computing stats of sets is done")

        Comparison=list(Comparisons.keys())[0]

        xaxis = False
        LegendPosition = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["LegendPosition"]
        if "xaxis" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            xaxis = True
            xticks = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xaxis"]["xticks"]
            xtickslabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xaxis"]["xtickslabels"]

        yaxis = False
        if "yaxis" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            yaxis = True
            yticks = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yaxis"]["yticks"]
            ytickslabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yaxis"]["ytickslabels"]

        if "PDFlabel_loc" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            PDFlabel_loc = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["PDFlabel_loc"]
        else:
            PDFlabel_loc = "upper center"
        if "Settingslabel_loc" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            Settingslabel_loc = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["Settingslabel_loc"]
        else:
            Settingslabel_loc = "upper center"

        if "colors" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            colors[Type_of_sets] = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["colors"]

        ncol = int(Fits_catalog[comparison_choice]
                    ["Comparisons"][Comparison]["ncol"])

        if len(flavors_to_plot) > 1:
            #if Comparison == "AbsolutesandRatio":
            fig = py.figure(figsize=(
                8.*ncol, 6.*int(round(len(flavors_to_plot)/(ncol*1.)+0.01))))  # , constrained_layout=True)
            #else:
            #    fig = py.figure(figsize=(8*ncol, 6), constrained_layout=True)
        else:
            fig = py.figure(figsize=(8, 6))  # ,constrained_layout=True)

        fig.tight_layout()

        if len(flavors_to_plot) > 1:
            gs = fig.add_gridspec(
                int(round(len(flavors_to_plot)/(ncol*1.)+0.01)), ncol)
        else:
            gs = fig.add_gridspec(1, 1)

        py.gcf().subplots_adjust(left=-0.1)

        axs = []
        axs2 = []
        p1s = []
        p2s = []
        ps = []
        labels = []
        for iSet, Setname in enumerate(Setsnames):
            X = np.linspace(1, Nreps[iSet], Nreps[iSet])
            #print (Setname+"")
            row = 0
            col = 0
            for ifl, fl in enumerate(flavors_to_plot):
                if UNCERTAINTY == "68CL":
                    UP = LHAPDFSets[Setname]["up68"][fl]
                    LOW = LHAPDFSets[Setname]["low68"][fl]
                elif UNCERTAINTY == "90CL":
                    UP = LHAPDFSets[Setname]["up90"][fl]
                    LOW = LHAPDFSets[Setname]["low90"][fl]
                elif UNCERTAINTY == "std":
                    UP = LHAPDFSets[Setname]["mean"][fl] + \
                        LHAPDFSets[Setname]["std"][fl]
                    LOW = LHAPDFSets[Setname]["mean"][fl] - \
                        LHAPDFSets[Setname]["std"][fl]

                if Type_of_sets == "FFs":
                    if len(flavors_to_plot) != 1:
                        dist = "zD^{("+hadron+")}_{i}"
                    else:
                        dist = "zD^{("+hadron+")}_{"+fl+"}"
                    xaxis_label = "z"
                elif Type_of_sets == "PDFs":
                    if len(flavors_to_plot) != 1:
                        dist = "xf^{(p)}"
                    else:
                        dist = "xf^{(p)}_{"+fl+"}"
                    xaxis_label = "x"
                elif Type_of_sets == "nPDFs":
                    if len(flavors_to_plot) != 1:
                        dist = "xf^{(A)}"
                    else:
                        dist = "xf^{(A)}_{"+fl+"}"
                    xaxis_label = "x"


                Nmem = Sets[Setname][fl].shape[0]
                Y=[]
                for irep in range(1, Nreps[iSet]+1):
                    #Y.append(np.std(Sets[Setname][fl][1:irep+1, :], axis=0))
                    Y.append(np.mean(Sets[Setname][fl][1:irep+1, :], axis=0))
                Y = np.array(Y)[:, 0] #/LHAPDFSets[Setname]["mean"][fl]*100.
                if "lss" in Fits_catalog[comparison_choice].keys():
                    ls = lss[Type_of_sets][iSet]
                else:
                    ls = "-"
                color = colors[Type_of_sets][iSet]
                ##
                row = int(ifl/ncol)
                col = int(ifl % ncol)
                ax = py.subplot(gs[row, col])
                axs.append(ax)
                
                ##
                if fl == LegendPosition:
                    label_suffix = ""
                    #if iSet == Ratio_den_Set and Comparison == "Ratio":
                    #    label_suffix = r" {\rm [ref]}"

                    p1 = axs[ifl].plot(X, Y, color=color, ls=ls, lw=1.5)
                    if comparison_choice == "RW_ex":
                        if iSet % 2 == 0:
                            p1s.append(p1[0])
                    else:
                        p1s.append(p1[0])

                    if Comparison == "NuclearRatio" or Comparison == "NuclearRatio_pull" or Comparison == "NuclearRatio_RelativeUncertainty":
                        LABEL = Setlabels[int((iSet+1)/2)-1]+label_suffix
                    else:
                        LABEL = Setlabels[iSet]+label_suffix

                    if comparison_choice == "RW_ex":
                        if iSet % 2 == 0:
                            labels.append(LABEL)
                    else:
                        labels.append(LABEL)
                    #lg = axs[ifl].legend(ps,labels,loc='best', title=r'{\rm \textbf{'+NUCLEUS+r'} \textbf{'+PTO+r'} ($Q=' + '{: .1f}'.format(
                    #    Q)+r'\, \, {\rm GeV}$)\\}', # \textbf{[Preliminary]}\\}',
                    #     fontsize=legend_fontsize, ncol=1, frameon=False, handletextpad=-1.8)
                    #lg.get_title().set_fontsize(fontsize=legend_fontsize)

                else:
                    axs[ifl].plot(X, Y, color=color, ls=ls, lw=1.5)

                ##
                #axs[ifl].set_xscale('log')
                """if "xlim" in Fits_catalog[comparison_choice]["Comparisons"][Comparison]:
                    xlim = Fits_catalog[comparison_choice]["Comparisons"][Comparison]['xlim']
                    if xlim[ifl]:
                        axs[ifl].set_xlim(xlim[ifl][0], xlim[ifl][1])
                else:
                    axs[ifl].set_xlim(xmin, xmax)"""
                axs[ifl].tick_params(direction='in', which='both')
                axs[ifl].tick_params(which='major', length=7)
                axs[ifl].tick_params(which='minor', length=4)

                ##
                if not ifl % ncol:
                    axs[ifl].set_ylabel(
                        r'{\rm \boldmath $<f>$}', fontsize=fontsize, rotation=90)
                        #r'{\rm \boldmath $\delta f/f [\%]$}', fontsize=fontsize, rotation=90)
                    axs[ifl].yaxis.set_label_coords(-0.11, 0.5)

                fl_label_scale = 1
                if fl == 'u^+ + d^+ + s^+':
                    fl_label_scale = 2.75

                #if len(flavors_to_plot) != 1:
                axs[ifl].text(0.075*fl_label_scale, 0.9, r'{\rm \boldmath $'+fl+'$}', horizontalalignment='center',
                                verticalalignment='center', transform=axs[ifl].transAxes, fontsize=fontsize)

                #https://stackoverflow.com/questions/44078409/matplotlib-semi-log-plot-minor-tick-marks-are-gone-when-range-is-large
                """locmaj = matplotlib.ticker.LogLocator(base=10.0, numticks=12)
                locmin = matplotlib.ticker.LogLocator(
                    base=10.0, subs=np.arange(0.1, 1., 0.1), numticks=12)
                axs[ifl].xaxis.set_major_locator(locmaj)
                axs[ifl].xaxis.set_minor_locator(locmin)
                axs[ifl].xaxis.set_minor_formatter(
                    matplotlib.ticker.NullFormatter())"""


                if int(ifl/ncol) >= int(len(flavors_to_plot)/ncol)-1:
                    axs[ifl].set_xlabel(
                        r'{\rm \boldmath Samples}', fontsize=fontsize)

        #ps = []
        #labels = []
        #for iSet, Setname in enumerate(Setsnames):
        #    ps.append((p2s[iSet][0], p1s[iSet][0]))
        #    labels.append(LABEL)

        if UNCERTAINTY == "68CL":
            #LABEL = r'{\rm {\large $~^{68\%~{\rm CL}}$} ~~' + Setlabels[iSet]+label_suffix
            UNCLABEL = [r'{\rm median}', r'{\rm 68\% CL}']
        elif UNCERTAINTY == "90CL":
            #LABEL = r'{\rm {\large $~^{68\%~{\rm CL}}$} ~~' + Setlabels[iSet]+label_suffix
            UNCLABEL = [r'{\rm median}', r'{\rm 90\% CL}']
        elif UNCERTAINTY == "std":
            #LABEL = r'{\rm {\large $~^{\pm~\sigma}$} ~~~~~' + Setlabels[iSet]+label_suffix
            UNCLABEL = [r'{\rm mean}', r'$\pm \sigma$']


        for ifl, fl in enumerate(flavors_to_plot):
            if fl == LegendPosition:

                if len(flavors_to_plot) != 1:
                    lg = axs[ifl].legend(p1s, labels, loc=PDFlabel_loc, title=r'{\rm $x='+str(X_value)+r'$\\}',  # \textbf{[Preliminary]}\\}',
                                            fontsize=legend_fontsize, ncol=1, frameon=False)  # , handletextpad=-1.8)
                    lg.get_title().set_fontsize(fontsize=legend_fontsize)

                    if ncol == 2:
                        adjacent_ifl = 1
                    elif ncol == 3:
                        adjacent_ifl = 3
                    axs[ifl+adjacent_ifl].plot(
                        np.NaN, np.NaN, color='black', ls='-', lw=1.5, label=r"{\rm Fit}")
                    axs[ifl+adjacent_ifl].plot(
                        np.NaN, np.NaN, color='black', ls='--', lw=1.5, label=r"{\rm Reweighting}")
                    lg2 = axs[ifl+adjacent_ifl].legend(loc=Settingslabel_loc, title=r'{\rm $Q=' + '{: .1f}'.format(
                        Q)+r'\, \, {\rm GeV}$\\}',  # \textbf{[Preliminary]}\\}',
                        fontsize=legend_fontsize, ncol=1, frameon=False)
                    #lg2 = axs[ifl+adjacent_ifl].legend([],[],loc='upper right', title=r'{\rm $Q=' + '{: .1f}'.format(
                    #    Q)+r'\, \, {\rm GeV}$\\'+UNCLABEL+r'}',  # \textbf{[Preliminary]}\\}',
                    #        fontsize=legend_fontsize, ncol=1, frameon=False, handletextpad=-1.8)
                    lg2.get_title().set_fontsize(fontsize=legend_fontsize)
                else:
                    lg = axs[ifl].legend(p1s, labels, loc=PDFlabel_loc, title=r'{\rm $x='+str(X_value)+r'$\\}',  # \textbf{[Preliminary]}\\}',
                        fontsize=legend_fontsize, ncol=1, frameon=False)  # , handletextpad=-1.8)
                    lg.get_title().set_fontsize(fontsize=legend_fontsize)

        py.tight_layout()
        py.savefig(outputname+'/'+comparison_choice+'_' + "x"+str(ixx)+"_"+
                    Type_of_sets+'_Q'+str(int(Q))+output_format)

        py.clf()
        py.cla()

        print("------")
