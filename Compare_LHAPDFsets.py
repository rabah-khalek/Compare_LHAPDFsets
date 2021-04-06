#-- Author: Rabah Abdul Khalek <rabah.khalek@gmail.com>
import matplotlib.ticker
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

colors={}

InputCard = sys.argv[1]
outputname = InputCard.split(".yaml")[0]
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

if comparison_choices[0]=="all":
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
    PTO = Fits_catalog[comparison_choice]["PTO"]
    hadron= " "
    if "hadron" in Fits_catalog[comparison_choice].keys():
        hadron = Fits_catalog[comparison_choice]["hadron"]

    if Fits_catalog['Global Settings'][Type_of_sets]["colors"] == "default":
        colors[Type_of_sets] = py.rcParams['axes.prop_cycle'].by_key()['color']
    else:
        colors[Type_of_sets] = Fits_catalog['Global Settings'][Type_of_sets]["colors"]

    if not os.path.isdir(outputname):
        os.system('mkdir '+outputname)
        
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

    for Comparison in Comparisons.keys():

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

        ncol = int(Fits_catalog[comparison_choice]["Comparisons"][Comparison]["ncol"])

        if len(flavors_to_plot)>1:
            #if Comparison == "AbsolutesandRatio":
            fig = py.figure(figsize=(
                8.*ncol, 6.*int(round(len(flavors_to_plot)/(ncol*1.)+0.01))))#, constrained_layout=True)
            #else:
            #    fig = py.figure(figsize=(8*ncol, 6), constrained_layout=True)
        else:
            fig=py.figure(figsize=(8,6))#,constrained_layout=True)

        fig.tight_layout()
        
        if len(flavors_to_plot)>1:
            gs = fig.add_gridspec(int(round(len(flavors_to_plot)/(ncol*1.)+0.01)), ncol)
        else:
            gs=fig.add_gridspec(1, 1)

        #py.gcf().subplots_adjust(wspace=0.5)
        

        axs = []
        axs2=[]
        for iSet, Setname in enumerate(Setsnames):
            #print (Setname+"")
            row=0
            col=0
            for ifl, fl in enumerate(flavors_to_plot):
                UP = LHAPDFSets[Setname]["mean"][fl]+LHAPDFSets[Setname]["std"][fl]
                LOW = LHAPDFSets[Setname]["mean"][fl]-LHAPDFSets[Setname]["std"][fl]

                if Type_of_sets == "FFs":
                    dist = "$zD^{"+hadron+"}_{q}$"
                    xaxis_label = "z"
                elif Type_of_sets == "PDFs":
                    dist = "$xf^{p}_{q}$"
                    xaxis_label = "x"
                elif Type_of_sets == "nPDFs":
                    dist = "$xf^{A}_{q}$"
                    xaxis_label = "x"


                if Comparison == "Absolutes":
                    Y = LHAPDFSets[Setname]["mean"][fl]
                    Y_minus = LOW
                    Y_plus = UP
                    ls="-"

                elif Comparison == "Relative Uncertainty":
                    Y = (UP-LOW)/LHAPDFSets[Setname]["mean"][fl]
                    Y_minus = None
                    Y_plus = None
                    dist="$\delta($"+dist+"$)\,[\%]$"
                    ls="-"

                elif Comparison == "Ratio":
                    Y = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    Y_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    Y_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    ls="--"

                elif Comparison == "AbsolutesandRatio":
                    Y = LHAPDFSets[Setname]["mean"][fl]
                    Y_minus = LOW
                    Y_plus = UP
                    ls="-"

                    Y2 = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    Y2_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    Y2_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    ls2="--"

                    dist1=dist
                    dist2="Ratio"

                ##
                if iSet == 0:
                    if Comparison == "AbsolutesandRatio":

                        row=int(ifl/ncol)
                        col=int(ifl%ncol)
                        gs_local = gs[row,col].subgridspec(3, 1,hspace=0.)
                        ax1 = fig.add_subplot(gs_local[:2])
                        ax2 = fig.add_subplot(gs_local[2])

                        axs.append(ax1)
                        axs2.append(ax2)
                    else:
                        row = int(ifl/ncol)
                        col = int(ifl % ncol)
                        ax = py.subplot(gs[row,col])
                        axs.append(ax)

                ##
                if fl == LegendPosition:
                    axs[ifl].plot(X, Y, color=colors[Type_of_sets][iSet], ls=ls, lw=1.5, label=Setlabels[iSet])

                    if Comparison != "Relative Uncertainty":
                        if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                            axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[Type_of_sets][iSet], edgecolor=colors[Type_of_sets][iSet], alpha=0.25, lw=0.1)

                    lg = axs[ifl].legend(loc='best', title=r'{\rm \textbf{'+PTO+r'} ($Q=' + '{: .1f}'.format(
                        Q)+r'\, \, {\rm GeV}$) \\}', fontsize=legend_fontsize, ncol=1, frameon=False)
                    lg.get_title().set_fontsize(fontsize=legend_fontsize)

                else:
                    axs[ifl].plot(X, Y, color=colors[Type_of_sets][iSet], ls=ls, lw=1.5)
                    if Comparison != "Relative Uncertainty":
                        if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                            axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=colors[Type_of_sets][iSet], edgecolor=colors[Type_of_sets][iSet], alpha=0.25, lw=0.1)

                if Comparison == "AbsolutesandRatio":
                    axs2[ifl].plot(X, Y2, color=colors[Type_of_sets][iSet], ls=ls2, lw=1.5)
                    axs2[ifl].fill_between(X, Y2_plus, Y2_minus, facecolor=colors[Type_of_sets][iSet], edgecolor=colors[Type_of_sets][iSet], alpha=0.25, lw=0.1)

                ##
                axs[ifl].set_xscale('log')
                axs[ifl].set_xlim(xmin, xmax)
                axs[ifl].tick_params(direction='in', which='both')
                axs[ifl].tick_params(which='major', length=7)
                axs[ifl].tick_params(which='minor', length=4)

                if Comparison == "AbsolutesandRatio":
                    axs2[ifl].set_xscale('log')
                    axs2[ifl].set_xlim(xmin, xmax)
                    axs2[ifl].tick_params(direction='in', which='both')
                    axs2[ifl].tick_params(which='major', length=7)
                    axs2[ifl].tick_params(which='minor', length=4)

                
                ##
                if not ifl%ncol:
                    axs[ifl].set_ylabel(r'{\rm \boldmath'+dist+'}', fontsize=fontsize, rotation=90)
                    axs[ifl].yaxis.set_label_coords(-0.075, 0.5)
                    if Comparison == "AbsolutesandRatio":
                        axs2[ifl].set_ylabel(r'{\rm \textbf{'+dist2+'}}', fontsize=fontsize, rotation=90)
                        axs2[ifl].yaxis.set_label_coords(-0.075, 0.5)
                
                axs[ifl].text(0.075, 0.9, r'{\rm \boldmath $'+fl+'$}' , horizontalalignment='center', verticalalignment='center', transform=axs[ifl].transAxes, fontsize=fontsize)

                #https://stackoverflow.com/questions/44078409/matplotlib-semi-log-plot-minor-tick-marks-are-gone-when-range-is-large
                locmaj = matplotlib.ticker.LogLocator(base=10.0, numticks=12)
                locmin = matplotlib.ticker.LogLocator(base=10.0,subs=np.arange(0.1,1.,0.1),numticks=12)
                axs[ifl].xaxis.set_major_locator(locmaj)
                axs[ifl].xaxis.set_minor_locator(locmin)
                axs[ifl].xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

                if Comparison == "AbsolutesandRatio":
                    axs2[ifl].xaxis.set_major_locator(locmaj)
                    axs2[ifl].xaxis.set_minor_locator(locmin)
                    axs2[ifl].xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

                if int(ifl/ncol) >= int(len(flavors_to_plot)/ncol)-1:
                    if Comparison == "AbsolutesandRatio":
                        axs2[ifl].set_xlabel(r'{\rm \boldmath $'+xaxis_label+r'$}', fontsize=fontsize)
                    else:
                        axs[ifl].set_xlabel(r'{\rm \boldmath $'+xaxis_label+r'$}', fontsize=fontsize)

                if Comparison == "AbsolutesandRatio":
                    if xaxis:
                        axs2[ifl].set_xticks(xticks)
                        axs2[ifl].set_xticklabels(xtickslabels)
                    if yaxis:
                        axs2[ifl].set_yticks(yticks)
                        axs2[ifl].set_yticklabels(ytickslabels)
                else:
                    if xaxis:
                        axs[ifl].set_xticks(xticks)
                        axs[ifl].set_xticklabels(xtickslabels)
                    if yaxis:
                        axs[ifl].set_yticks(yticks)
                        axs[ifl].set_yticklabels(ytickslabels)


                ##
                if Comparison == "AbsolutesandRatio":
                    axs[ifl].set_xticklabels([])
                if int(ifl/ncol) < int(len(flavors_to_plot)/ncol)-1:
                    axs[ifl].set_xticklabels([])
                    if Comparison == "AbsolutesandRatio":
                        axs2[ifl].set_xticklabels([])

                if "ylim" in Fits_catalog[comparison_choice]["Comparisons"][Comparison]:
                    ylim = Fits_catalog[comparison_choice]["Comparisons"][Comparison]['ylim']
                    if ylim[ifl]:
                        axs[ifl].set_ylim(ylim[ifl][0], ylim[ifl][1])
                if Comparison == "AbsolutesandRatio":
                    axs2[ifl].set_ylim(-0.25, 2.25)
                    axs2[ifl].set_yticks([0,1,2])
                    axs2[ifl].set_yticklabels([r'$\rm 0$', r'$\rm 1$', r'$\rm 2$'])



        py.tight_layout()
        py.savefig(outputname+'/'+comparison_choice+'_'+Comparison.split(" ")[0] +
                Type_of_sets+'_Q'+str(int(Q))+output_format)

        py.clf()
        py.cla()

    print("------")
