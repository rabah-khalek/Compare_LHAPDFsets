#-- Author: Rabah Abdul Khalek <rabah.khalek@gmail.com>

import os
import sys
import numpy as np
import yaml
import matplotlib.pyplot as py
from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
import warnings
import matplotlib.gridspec as gridspec
warnings.filterwarnings("ignore")
import src.sets as SETS

#! flavours available
#
# r'$\gamma$': 0, r'$\Sigma$': 1, r'$g$': 2, r'$V$': 3, r'$V_3$': 4, r'$V_8$': 5, r'$V_{15}$': 6,
# r'$V_{24}$': 7, r'$V_{35}$': 8, r'$T_{3}$': 9, r'$T_{3}$': 10, r'$T_{15}$': 11, r'$T_{24}$': 12, r'$T_{35}$': 13}
# r'$\bar{t}$': 0, r'$\bar{b}$': 1, r'$\bar{c}$': 2, r'$\bar{s}$': 3, r'$\bar{u}$': 4, r'$\bar{d}$': 5,
# r'$g$': 6, r'$d$': 7, r'$u$': 8, r'$s$': 9, r'$c$': 10, r'$b$': 11, r'$t$': 12, r'$\gamma$': 13}
# r'$F_2^{LO}$' r'$u^+$' r'$d^+$' r'$s^+$' r'$c^+$' r'$b^+$' r'$t^+$' r'$u^-$' r'$d^-$' r'$s^-$' r'$c^-$' r'$b^-$' r'$t^-$'

Ratio_den_Set = 0  # 0 for the first PDF to be chosen as denominator in the ratio

#---- plotting settings
label_ncol = 1
ratio_label_ncol = 1
colors = py.rcParams['axes.prop_cycle'].by_key()['color']
fontsize = 20
legend_fontsize = 15
rc('xtick', labelsize=fontsize)
rc('ytick', labelsize=fontsize)
py.rcParams['legend.title_fontsize'] = 'xx-large'

#---- to modify
Type_of_sets = "PDFs"
comparison_choices = ["test"]
# "Absolutes", "Relative Uncertainty", "Ratio"
comparison_types = ["Absolutes", "Relative Uncertainty", "Ratio"]
plots_format = ["vertical", "horizontal"]  # "vertical","horizontal"


Fits_catalog = None
with open(Type_of_sets+"_fits.yaml") as f:
    Fits_catalog = yaml.safe_load(f)

if comparison_choices[0]=="all":
    comparison_choices = Fits_catalog.keys()

for comparison_choice in comparison_choices:
    print("\n---"+comparison_choice+"---")

    Setsnames = Fits_catalog[comparison_choice]["Setsnames"]
    Setlabels = Fits_catalog[comparison_choice]["Setlabels"]
    Error_type = Fits_catalog[comparison_choice]["Error_type"] 
    Nreps = Fits_catalog[comparison_choice]["Nreps"]
    flavors_to_plot = Fits_catalog[comparison_choice]["flavors_to_plot"]

    Q = Fits_catalog[comparison_choice]["Q"]
    Q2 = Q**2  

    xmin, xmax, nx = Fits_catalog[comparison_choice]["x"][0], Fits_catalog[
        comparison_choice]["x"][1], Fits_catalog[comparison_choice]["x"][2]
    X = np.logspace(np.log10(xmin), np.log10(xmax), nx)


    LHAPDFSets = {}
    for Setnames in Setsnames:
        for iSet, Setname in enumerate(Setnames):
            print("Loading "+Setname+"")
            Sets = SETS.Get(Setname, X, Q, Nreps[iSet]+1)
            LHAPDFSets[Setname] = SETS.GetStats(Sets, Error_type[iSet])

    print("Computing stats of sets is done")

    ##VERTICAL VERSION
    if "vertical" in plots_format:
        for comparison_type in comparison_types:

            py.figure(figsize=(8, 6*len(flavors_to_plot)))
            gs = gridspec.GridSpec(int(len(flavors_to_plot)),len(Setsnames))
            gs.update(wspace=0.025, hspace=0.05) # set the spacing between axes. 

            print("Plotting vertical "+comparison_type+"")

            axs = []
            for iSets, Setnames in enumerate(Setsnames):
                for iSet, Setname in enumerate(Setnames):

                    #print (Setname+"")
                    for ifl, fl in enumerate(flavors_to_plot):
                        UP = LHAPDFSets[Setname]["mean"][fl]+LHAPDFSets[Setname]["std"][fl]
                        LOW = LHAPDFSets[Setname]["mean"][fl]-LHAPDFSets[Setname]["std"][fl]

                        if comparison_type == "Absolutes":
                            Y = LHAPDFSets[Setname]["mean"][fl]
                            Y_minus = LOW
                            Y_plus = UP

                        elif comparison_type == "Relative Uncertainty":
                            Y = (UP-LOW)/LHAPDFSets[Setname]["mean"][fl]
                            Y_minus = None
                            Y_plus = None

                        elif comparison_type == "Ratio":
                            Y = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]
                            Y_minus = LOW / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]
                            Y_plus = UP / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]

                        ##
                        if iSet == 0:
                            ax = py.subplot(gs[ifl*len(Setsnames)+iSets])
                            axs.append(ax)

                        ##
                        if iSets!=0:
                            axs[ifl].set_yticklabels([])

                        ##
                        if ifl == 0 and iSets == 0:
                            axs[ifl].plot(X, Y, color=colors[iSet], ls='-', lw=1.5, label=Setlabels[iSet])
                            if comparison_type != "Relative Uncertainty":
                                if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                    axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)
                            axs[ifl].legend(loc='best', fontsize=legend_fontsize, ncol=label_ncol, frameon=False)
                        else:
                            axs[ifl].plot(X, Y, color=colors[iSet], ls='-', lw=1.5)
                            if comparison_type != "Relative Uncertainty":
                                if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                    axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)
                            
                        ##
                        axs[ifl].set_xscale('log')
                        axs[ifl].set_xlim(xmin, xmax)
                        axs[ifl].tick_params(direction='in', which='both')
                        axs[ifl].tick_params(which='major', length=5)
                        axs[ifl].tick_params(which='minor', length=2)
                        
                        ##
                        if iSets == 0:
                            axs[ifl].set_ylabel(r'{\rm \boldmath'+fl+'}', fontsize=fontsize, rotation=0)
                            axs[ifl].yaxis.set_label_coords(0.05, 0.925)
                        
                        ##
                        if ifl == 0:
                            axs[ifl].set_title(r'{\rm \textbf{'+Type_of_sets+' '+comparison_type+r'} ($Q=' +
                                            '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$) \\}', fontsize=fontsize)
                            axs[ifl].set_xticklabels([])
                        elif ifl == len(flavors_to_plot)-1:
                            axs[ifl].set_xlabel(r'{\rm \boldmath $x$}', fontsize=fontsize)
                            axs[ifl].xaxis.set_label_coords(0.95, 0.075)
                        else:
                            axs[ifl].set_xticklabels([])


            py.tight_layout()
            py.savefig(Type_of_sets+'_figs/vertical/'+comparison_choice+'_'+comparison_type.split(" ")[0]+
                    Type_of_sets+'_Q'+str(int(Q))+'.pdf')

            py.clf()
            py.cla()

    ##HORIZONTAL VERSION
    if "horizontal" in plots_format:
        for comparison_type in comparison_types:

            fig = py.figure(figsize=(8*len(flavors_to_plot), 6))
            gs = gridspec.GridSpec(len(Setsnames), int(len(flavors_to_plot)))
            #gs.update(wspace=0.025, hspace=0.05) # set the spacing between axes. 

            print("Plotting horizontal "+comparison_type+"")

            axs = []
            for iSets, Setnames in enumerate(Setsnames):
                for iSet, Setname in enumerate(Setnames):

                    #print (Setname+"")
                    for ifl, fl in enumerate(flavors_to_plot):
                        UP = LHAPDFSets[Setname]["mean"][fl]+LHAPDFSets[Setname]["std"][fl]
                        LOW = LHAPDFSets[Setname]["mean"][fl]-LHAPDFSets[Setname]["std"][fl]

                        if comparison_type == "Absolutes":
                            Y = LHAPDFSets[Setname]["mean"][fl]
                            Y_minus = LOW
                            Y_plus = UP

                        elif comparison_type == "Relative Uncertainty":
                            Y = (UP-LOW)/LHAPDFSets[Setname]["mean"][fl]
                            Y_minus = None
                            Y_plus = None

                        elif comparison_type == "Ratio":
                            Y = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]
                            Y_minus = LOW / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]
                            Y_plus = UP / LHAPDFSets[Setnames[Ratio_den_Set]]["mean"][fl]

                        ##
                        if iSet == 0:
                            ax = py.subplot(gs[iSets*len(Setsnames)+ifl])
                            axs.append(ax)

                        ##
                        if iSets!=0:
                            axs[ifl].set_yticklabels([])

                        ##
                        if ifl == 0 and iSets == 0:
                            axs[ifl].plot(X, Y, color=colors[iSet], ls='-', lw=1.5, label=Setlabels[iSet])
                            if comparison_type != "Relative Uncertainty":
                                if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                    axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)
                            axs[ifl].legend(loc='best', fontsize=legend_fontsize, ncol=label_ncol, frameon=False)
                        else:
                            axs[ifl].plot(X, Y, color=colors[iSet], ls='-', lw=1.5)
                            if comparison_type != "Relative Uncertainty":
                                if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                    axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)
                            
                        ##
                        axs[ifl].set_xscale('log')
                        axs[ifl].set_xlim(xmin, xmax)
                        axs[ifl].tick_params(direction='in', which='both')
                        axs[ifl].tick_params(which='major', length=5)
                        axs[ifl].tick_params(which='minor', length=2)
                        
                        ##
                        axs[ifl].set_ylabel(r'{\rm \boldmath'+fl+'}', fontsize=fontsize, rotation=0)
                        axs[ifl].yaxis.set_label_coords(0.05, 0.925)
                        #if ifl != 0:
                        #    axs[ifl].set_yticklabels([])


                        axs[ifl].set_xlabel(r'{\rm \boldmath $x$}', fontsize=fontsize)
                        axs[ifl].xaxis.set_label_coords(0.95, 0.075)
                            
            fig.suptitle(r'{\rm \textbf{'+Type_of_sets+' '+comparison_type+r'} ($Q=' +
                        '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$)}', y=0.96, fontsize=fontsize)
            py.tight_layout()
            py.savefig(Type_of_sets+'_figs/horizontal/'+comparison_choice+'_'+comparison_type.split(" ")[0]+
                    Type_of_sets+'_Q'+str(int(Q))+'.pdf')

            py.clf()
            py.cla()

    print("------")
