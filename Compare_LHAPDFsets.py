#-- Author: Rabah Abdul Khalek <rabah.khalek@gmail.com>
import sys, os
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

Ratio_den_Set = 0  # 0 for the first PDF to be chosen as denominator in the ratio

#---- plotting settings
label_ncol = 1
ratio_label_ncol = 1
fontsize = 20
legend_fontsize = 15
rc('xtick', labelsize=fontsize)
rc('ytick', labelsize=fontsize)
py.rcParams['legend.title_fontsize'] = 'xx-large'

#---- to modify

comparison_choices = ["all"]
# "Absolutes", "Relative Uncertainty", "Ratio"
colors={}

InputCard = sys.argv[1]
outputname = InputCard.split(".yaml")[0]
Fits_catalog = None
with open(InputCard) as f:
    Fits_catalog = yaml.safe_load(f)

if comparison_choices[0]=="all":
    comparison_choices = list(Fits_catalog.keys())

comparison_choices.remove("Global Settings")
for comparison_choice in comparison_choices:
    print("\n---"+comparison_choice+"---")

    Setsnames = Fits_catalog[comparison_choice]["Setsnames"]
    Setlabels = Fits_catalog[comparison_choice]["Setlabels"]
    Error_type = Fits_catalog[comparison_choice]["Error_type"] 
    Nreps = Fits_catalog[comparison_choice]["Nreps"]
    flavors_to_plot = Fits_catalog[comparison_choice]["flavors_to_plot"]
    Comparisons = Fits_catalog[comparison_choice]["Comparisons"]
    plots_format = Fits_catalog[comparison_choice]["plots_format"]
    Type_of_sets = Fits_catalog[comparison_choice]["Type_of_sets"]
    xaxis_label = Fits_catalog[comparison_choice]["xaxis_label"]
    hadron= " "
    if "hadron" in Fits_catalog[comparison_choice].keys():
        hadron = Fits_catalog[comparison_choice]["hadron"]

    if Fits_catalog['Global Settings'][Type_of_sets]["colors"] == "default":
        colors[Type_of_sets] = py.rcParams['axes.prop_cycle'].by_key()['color']
    else:
        colors[Type_of_sets] = Fits_catalog['Global Settings'][Type_of_sets]["colors"]

    if not os.path.isdir(outputname):
        os.system('mkdir '+outputname)
    if not os.path.isdir(outputname + '/vertical'):
        os.system('mkdir '+outputname + '/vertical')
    if not os.path.isdir(outputname + '/horizontal'):
        os.system('mkdir '+outputname + '/horizontal')
        
    
    Q = Fits_catalog[comparison_choice]["Q"]
    Q2 = Q**2  

    xmin, xmax, nx = Fits_catalog[comparison_choice]["x"][0], Fits_catalog[
        comparison_choice]["x"][1], Fits_catalog[comparison_choice]["x"][2]
    X = np.logspace(np.log10(xmin), np.log10(xmax), nx)


    LHAPDFSets = {}
    for iSet, Setname in enumerate(Setsnames):
        print("Loading "+Setname+"")
        if not Setname in LHAPDFSets.keys():
            Sets = SETS.Get(Setname, X, Q, Nreps[iSet]+1)
            LHAPDFSets[Setname] = SETS.GetStats(Sets, Error_type[iSet])

    print("Computing stats of sets is done")

    ##VERTICAL VERSION
    for plot_format in plots_format:
        for Comparison in Comparisons.keys():

            xticklabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xticklabels"]
            yticklabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yticklabels"]
            legend = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["legend"]
            title = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["title"]
            xlabel = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xlabel"]
            ylabel = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["ylabel"]
            xticklabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xticklabels"]
            yticklabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yticklabels"]
            xaxis = False
            if "xaxis" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
                xaxis = True
                xticks = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xaxis"]["xticks"]
                xtickslabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["xaxis"]["xtickslabels"]

            yaxis = False
            if "yaxis" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
                yaxis = True
                yticks = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yaxis"]["yticks"]
                ytickslabels = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["yaxis"]["ytickslabels"]

            if plot_format=="vertical":
                py.figure(figsize=(8, 6*len(flavors_to_plot)))
                gs = gridspec.GridSpec(int(len(flavors_to_plot)),1)
                gs.update(wspace=0.025, hspace=0.02) # set the spacing between axes. 
                py.gcf().subplots_adjust(left=0.15, right=0.95, top=0.99)
                print("Plotting vertical "+Comparison+"")
            elif plot_format=="horizontal":
                fig = py.figure(figsize=(8*len(flavors_to_plot), 6))
                gs = gridspec.GridSpec(1, int(len(flavors_to_plot)))
                if ylabel == 'inside' or ylabel == 'none':
                    gs.update(wspace=0.1)  # set the spacing between axes.
                elif ylabel == 'outside':
                    gs.update(wspace=0.25)  # set the spacing between axes.
                py.subplots_adjust(left=0.1, right=0.99, top=0.99)
                if not xticklabels:
                    py.subplots_adjust(bottom=0.005)

                print("Plotting horizontal "+Comparison+"")

            axs = []
            for iSet, Setname in enumerate(Setsnames):
                #print (Setname+"")
                for ifl, fl in enumerate(flavors_to_plot):
                    UP = LHAPDFSets[Setname]["mean"][fl]+LHAPDFSets[Setname]["std"][fl]
                    LOW = LHAPDFSets[Setname]["mean"][fl]-LHAPDFSets[Setname]["std"][fl]

                    if Comparison == "Absolutes":
                        Y = LHAPDFSets[Setname]["mean"][fl]
                        Y_minus = LOW
                        Y_plus = UP
                        Comparison_title = Type_of_sets
                        ls="-"

                    elif Comparison == "Relative Uncertainty":
                        Y = (UP-LOW)/LHAPDFSets[Setname]["mean"][fl]
                        Y_minus = None
                        Y_plus = None
                        Comparison_title = Comparison
                        ls="-"

                    elif Comparison == "Ratio":
                        Y = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Comparison_title = Comparison
                        ls="--"

                    if Type_of_sets == "FFs":
                        dist = "$zD^{"+hadron+"}_{"+fl+"}$"
                    elif Type_of_sets == "PDFs":
                        dist = "$xf^{p}_{"+fl+"}$"
                    elif Type_of_sets == "nPDFs":
                        dist = "$xf^{A}_{"+fl+"}$"

                    ##
                    if iSet == 0:
                        ax = py.subplot(gs[ifl])
                        axs.append(ax)

                    ##
                    if ifl == 0 and legend:
                        axs[ifl].plot(X, Y, color=colors[iSet], ls=ls, lw=1.5, label=Setlabels[iSet])

                        if Comparison != "Relative Uncertainty":
                            if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)

                        axs[ifl].legend(loc='best', title=r'{\rm \textbf{'+Comparison_title+r'} ($Q=' + '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$) \\}',fontsize=legend_fontsize, ncol=label_ncol, frameon=False)
                    else:
                        axs[ifl].plot(X, Y, color=colors[iSet], ls=ls, lw=1.5)
                        if Comparison != "Relative Uncertainty":
                            if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                                axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[iSet], edgecolor=colors[iSet], alpha=0.25, lw=0.1)
                        if ifl == 0 and title:
                            axs[ifl].legend(loc='best', title=r'{\rm \textbf{'+Comparison_title+r'} ($Q=' + '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$) \\}',fontsize=legend_fontsize, ncol=label_ncol, frameon=False)
                    ##
                    axs[ifl].set_xscale('log')
                    axs[ifl].set_xlim(xmin, xmax)
                    axs[ifl].tick_params(direction='in', which='both')
                    axs[ifl].tick_params(which='major', length=5)
                    axs[ifl].tick_params(which='minor', length=2)
                    
                    ##
                    if ylabel != 'none':
                        axs[ifl].set_ylabel(r'{\rm \boldmath'+dist+'}', fontsize=fontsize, rotation=0)
                    if ylabel == 'inside':
                        axs[ifl].yaxis.set_label_coords(0.05, 0.925)
                    elif ylabel == 'outside':
                        axs[ifl].yaxis.set_label_coords(-0.125, 0.5)
                    
                    ##
                    if plot_format=="vertical":
                        if ifl == 0:
                            #if title: axs[ifl].set_title(r'{\rm \textbf{$'+hadron+'$ '+Type_of_sets+' '+Comparison_title+r'} ($Q=' +
                            #                '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$) \\}', fontsize=fontsize)
                            axs[ifl].set_xticklabels([])
                        elif ifl == len(flavors_to_plot)-1:
                            axs[ifl].set_xlabel(
                                r'{\rm \boldmath $'+xaxis_label+r'$}', fontsize=fontsize)
                            if xlabel == 'inside':
                                axs[ifl].xaxis.set_label_coords(0.95, 0.075)

                            if xaxis:
                                axs[ifl].set_xticks(xticks)
                                axs[ifl].set_xticklabels(xtickslabels)
                        else:
                            axs[ifl].set_xticklabels([])
                            if yaxis:
                                axs[ifl].set_yticks(yticks)
                                axs[ifl].set_yticklabels(ytickslabels)

                    elif plot_format=="horizontal":
                        #if title:
                        #    fig.suptitle(r'{\rm \textbf{$'+hadron+'$ '+Type_of_sets+' '+Comparison_title+r'} ($Q=' +
                        #                 '{: .1f}'.format(Q)+r'\, \, {\rm GeV}$)}', y=0.96, fontsize=fontsize)
                        if xlabel != "none":
                            axs[ifl].set_xlabel(r'{\rm \boldmath $'+xaxis_label+r'$}', fontsize=fontsize)
                        if xlabel == 'inside':
                            axs[ifl].xaxis.set_label_coords(0.95, 0.075)

                        if xaxis:
                            axs[ifl].set_xticks(xticks)
                            axs[ifl].set_xticklabels(xtickslabels)
                        if yaxis:
                            axs[ifl].set_yticks(yticks)
                            axs[ifl].set_yticklabels(ytickslabels)
                    ##
                    if not xticklabels:
                        axs[ifl].set_xticklabels([])
                    if not yticklabels:
                        axs[ifl].set_yticklabels([])


            py.tight_layout()
            py.savefig(outputname+'/'+plot_format+'/'+comparison_choice+'_'+Comparison.split(" ")[0] +
                    Type_of_sets+'_Q'+str(int(Q))+'.pdf')

            py.clf()
            py.cla()

    print("------")
