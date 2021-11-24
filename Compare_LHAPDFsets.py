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

N1s = ["_N1", "CT14nlo", "nCTEQ15WZSIH_1_1"]

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

    Sets={}
    neutron_Sets={}
    nonuclear_Sets={}
    LHAPDFSets = {}
    neutron_LHAPDFSets = {}
    Y_pull={}
    Y_rel={}
    Nset = 0
    for iSet, Setname in enumerate(Setsnames):
        print("Loading "+Setname+"")
        if not Setname in LHAPDFSets.keys():
            Sets[Setname] = SETS.Get(Setname, X, Q, Nreps[iSet]+1)
            LHAPDFSets[Setname] = SETS.GetStats(Sets[Setname], Error_type[iSet])

            if "NuclearRatio" in Comparisons.keys():
                neutron_Sets[Setname]  = SETS.Get(Setname, X, Q, Nreps[iSet]+1, True)
                #nonuclear_Sets[Setname] = {}
                neutron_LHAPDFSets[Setname]  = SETS.GetStats(neutron_Sets[Setname] , Error_type[iSet])

            if "NuclearRatio_pull" in Comparisons.keys() and (not any(ext in Setname for ext in N1s) or Setname=="EPPS16nlo_CT14nlo_Pb208"):
                Y_pull[Setname] = {}

            if "NuclearRatio_RelativeUncertainty" in Comparisons.keys() and (not any(ext in Setname for ext in N1s) or Setname == "EPPS16nlo_CT14nlo_Pb208"):
                Y_rel[Setname] = {}
        Nset+=1

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
            
        if "PDFlabel_loc" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            PDFlabel_loc = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["PDFlabel_loc"]
        else:
            PDFlabel_loc = "upper center"
        if "Settingslabel_loc" in Fits_catalog[comparison_choice]["Comparisons"][Comparison].keys():
            Settingslabel_loc = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["Settingslabel_loc"]
        else:
            Settingslabel_loc = "upper center"

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
        p1s=[]
        p2s=[]
        ps = []
        labels = []
        for iSet, Setname in enumerate(Setsnames):
            #print (Setname+"")
            row=0
            col=0
            for ifl, fl in enumerate(flavors_to_plot):
                if UNCERTAINTY=="68CL":
                    UP = LHAPDFSets[Setname]["up68"][fl]
                    LOW = LHAPDFSets[Setname]["low68"][fl]
                elif UNCERTAINTY=="90CL":
                    UP = LHAPDFSets[Setname]["up90"][fl]
                    LOW = LHAPDFSets[Setname]["low90"][fl]
                elif UNCERTAINTY=="std":
                    UP = LHAPDFSets[Setname]["mean"][fl]+LHAPDFSets[Setname]["std"][fl]
                    LOW = LHAPDFSets[Setname]["mean"][fl] - LHAPDFSets[Setname]["std"][fl]

                if Type_of_sets == "FFs":
                    dist = "$zD^{("+hadron+")}_{i}$"
                    xaxis_label = "z"
                elif Type_of_sets == "PDFs":
                    dist = "$xf^{(p)}_{i}$"
                    xaxis_label = "x"
                elif Type_of_sets == "nPDFs":
                    dist = "$xf^{(A)}_{i}$"
                    xaxis_label = "x"


                if Comparison == "Absolutes":
                    if UNCERTAINTY == "68CL" or UNCERTAINTY == "90CL":
                        Y = LHAPDFSets[Setname]["median"][fl]
                    elif UNCERTAINTY=="std":
                        Y = LHAPDFSets[Setname]["mean"][fl]
                    Y_minus = LOW
                    Y_plus = UP
                    ls="-"
                    color = colors[Type_of_sets][iSet]

                elif Comparison == "Relative Uncertainty":
                    if UNCERTAINTY == "68CL" or UNCERTAINTY == "90CL":
                        Y = (UP-LOW)/LHAPDFSets[Setname]["median"][fl]
                    elif UNCERTAINTY == "std":
                        Y = (UP-LOW)/LHAPDFSets[Setname]["mean"][fl]

                    Y_minus = None
                    Y_plus = None
                    dist="$\delta($"+dist+"$)\,[\%]$"
                    ls="-"
                    temp_colors = ['m', 'c', 'y', 'k']
                    color = temp_colors[iSet]  # colors[Type_of_sets][iSet]

                elif Comparison == "Ratio":
                    if UNCERTAINTY == "68CL" or UNCERTAINTY == "90CL":
                        Y = LHAPDFSets[Setname]["median"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                        Y_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                        Y_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                    elif UNCERTAINTY == "std":
                        Y = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    ls="--"

                    if Type_of_sets == "FFs":
                        dist_den = r"$zD^{("+hadron+") {\rm [ref]}}_{i}$"
                    elif Type_of_sets == "PDFs":
                        dist_den = r"$xf^{(p) {\rm [ref]}}_{i}$"
                    elif Type_of_sets == "nPDFs":
                        dist_den = r"$xf^{(A) {\rm [ref]}}_{i}$"

                    # dist=dist+"/"+dist+" [ref]"
                    dist=dist+"/"+dist_den
                    temp_colors = ['m', 'c', 'y', 'k']
                    color = temp_colors[iSet] #colors[Type_of_sets][iSet]

                elif Comparison == "AbsolutesandRatio":
                    if UNCERTAINTY == "68CL" or UNCERTAINTY == "90CL":
                        Y = LHAPDFSets[Setname]["median"][fl]
                    elif UNCERTAINTY == "std":
                        Y = LHAPDFSets[Setname]["mean"][fl]
                    Y_minus = LOW
                    Y_plus = UP
                    ls="-"

                    if UNCERTAINTY == "68CL" or UNCERTAINTY == "90CL":
                        Y2 = LHAPDFSets[Setname]["median"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                        Y2_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                        Y2_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["median"][fl]
                    elif UNCERTAINTY == "std":
                        Y2 = LHAPDFSets[Setname]["mean"][fl] / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y2_minus = LOW / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                        Y2_plus = UP / LHAPDFSets[Setsnames[Ratio_den_Set]]["mean"][fl]
                    ls2="--"

                    dist1=dist #+r" $\pm 1-\sigma$"
                    dist2="Ratio"
                    color = colors[Type_of_sets][iSet]
                
                elif Comparison == "NuclearRatio":
                    if any(ext in Setname for ext in N1s) and Setname!="EPPS16nlo_CT14nlo_Pb208":

                        A = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["A"]
                        Z = Fits_catalog[comparison_choice]["Comparisons"][Comparison]["Z"]
                        
                        if Error_type[iSet]=="MC":
                            nonuclear_Sets[fl] = (
                                1./A)*(Z*Sets[Setname][fl]+(A-Z)*neutron_Sets[Setname][fl])
                        elif "hessian" in Error_type[iSet]:
                            #if "nCTEQ15" in Setname:
                            #    nonuclear_Sets[fl] = LHAPDFSets[Setname]["median"][fl] #Sets[Setname][fl] #
                            #else:
                            nonuclear_Sets[fl] = (
                                    1./A)*(Z*LHAPDFSets[Setname]["median"][fl]+(A-Z)*neutron_LHAPDFSets[Setname]["median"][fl])
                        color = colors[Type_of_sets][iSet]
                    else:
                        if Error_type[iSet]=="MC":
                            Nmem = Sets[Setname][fl].shape[0]
                            Y_rep = Sets[Setname][fl]/nonuclear_Sets[fl]
                            if UNCERTAINTY == "68CL":
                                Y = np.median(Y_rep[1:Nmem, :], axis=0)  # Y_rep[0, :]
                                Y_minus = np.nanpercentile(
                                    Y_rep[1:Nmem, :], 16., axis=0)
                                Y_plus = np.nanpercentile(
                                    Y_rep[1:Nmem, :], 84., axis=0)
                                
                            elif UNCERTAINTY == "90CL":
                                Y = np.median(Y_rep[1:Nmem, :], axis=0)  # Y_rep[0, :]
                                Y_minus = np.nanpercentile(
                                    Y_rep[1:Nmem, :], 5., axis=0)
                                Y_plus = np.nanpercentile(
                                    Y_rep[1:Nmem, :], 95., axis=0)
                                
                            elif UNCERTAINTY == "std":
                                Y = np.mean(Y_rep[1:Nmem, :], axis=0)
                                Y_std = np.std(Y_rep[1:Nmem, :], axis=0)
                                Y_minus = Y-Y_std
                                Y_plus = Y+Y_std
                                
                        elif "hessian" in Error_type[iSet]:
                            #!to check
                            if "nCTEQ15" in Setname:
                                Y = (1./A)*(Z*LHAPDFSets[Setname]["median"][fl]+(
                                    A-Z)*neutron_LHAPDFSets[Setname]["median"][fl])/nonuclear_Sets[fl]
                                Nmem = Sets[Setname][fl].shape[0]
                                Y_rep = (Z*Sets[Setname][fl]+(A-Z)*neutron_Sets[Setname][fl])/((Z*Sets["nCTEQ15WZSIH_1_1"][fl]+(A-Z)*neutron_Sets["nCTEQ15WZSIH_1_1"][fl]))
                                std = np.zeros(Sets[Setname][fl].shape[1])
                                for im in range(1, Nmem):
                                    f = Y_rep[im, :]
                                    std += (f-Y )**2
                                std=np.sqrt(std)
                            #the user should know if the set correspond to 68 or
                            #90 from the .info file
                                if UNCERTAINTY=="68CL":
                                    Y_minus = Y-std/1.644854
                                    Y_plus = Y+std/1.644854
                                elif UNCERTAINTY == "90CL":
                                    Y_minus = Y-std
                                    Y_plus = Y+std
                            elif "EPPS16" in Setname:
                                Y = LHAPDFSets[Setname]["median"][fl]/nonuclear_Sets[fl]
                                Nmem = Sets[Setname][fl].shape[0]
                                Y_rep = Sets[Setname][fl]/nonuclear_Sets[fl]
                                std = np.zeros(Sets[Setname][fl].shape[1])
                                for im in range(0, int((Nmem-1)/2)):
                                    fp = Y_rep[2*im+1, :]
                                    fm = Y_rep[2*im+2, :]
                                    std += (fp-fm)**2
                                std=0.5*np.sqrt(std)
                            #the user should know if the set correspond to 68 or
                            #90 from the .info file
                                if UNCERTAINTY=="68CL":
                                    Y_minus = Y-std/1.644854
                                    Y_plus = Y+std/1.644854
                                elif UNCERTAINTY == "90CL":
                                    Y_minus = Y-std
                                    Y_plus = Y+std
                                    
                            else:
                                Y = LHAPDFSets[Setname]["median"][fl]/nonuclear_Sets[fl]
                                if UNCERTAINTY == "68CL":
                                    Y_plus= LHAPDFSets[Setname]["up68"][fl]/nonuclear_Sets[fl]
                                    Y_minus= LHAPDFSets[Setname]["low68"][fl]/nonuclear_Sets[fl]
                                elif UNCERTAINTY == "90CL":
                                    Y_plus= LHAPDFSets[Setname]["up90"][fl]/nonuclear_Sets[fl]
                                    Y_minus= LHAPDFSets[Setname]["low90"][fl]/nonuclear_Sets[fl]
                                

                        #Pull on R
                        if "NuclearRatio_pull" in Comparisons.keys():
                            Y_pull[Setname][fl] = (Y - 1)/(Y_plus-Y)
                        #Relative uncertainty on R
                        if "NuclearRatio_RelativeUncertainty" in Comparisons.keys():
                            Y_rel[Setname][fl] = (Y_plus-Y_minus)/Y
                            
                        ls = "-"

                        dist = "$R^{(A)}_{i}$"
                        color = colors[Type_of_sets][int((iSet+1)/2)-1]

                elif Comparison == "NuclearRatio_pull" and (not any(ext in Setname for ext in N1s) or Setname=="EPPS16nlo_CT14nlo_Pb208"):

                    Y=Y_pull[Setname][fl]
                    Y_minus=Y_pull[Setname][fl]
                    Y_plus = Y_pull[Setname][fl]

                    dist = r" $P_i\left[R^{(A)}\right]$"
                    color = colors[Type_of_sets][int((iSet+1)/2)-1]

                elif Comparison == "NuclearRatio_RelativeUncertainty" and not any(ext in Setname for ext in N1s) or Setname == "EPPS16nlo_CT14nlo_Pb208":

                    Y = Y_rel[Setname][fl]
                    Y_minus = Y_rel[Setname][fl]
                    Y_plus = Y_rel[Setname][fl]

                    dist = r" $\delta(R_i^{(A)})\,[\%]$"
                    color = colors[Type_of_sets][int((iSet+1)/2)-1]
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

                if Comparison == "NuclearRatio" and any(ext in Setname for ext in N1s) and Setname!="EPPS16nlo_CT14nlo_Pb208":
                    continue

                if Comparison == "NuclearRatio_pull" and any(ext in Setname for ext in N1s) and Setname!="EPPS16nlo_CT14nlo_Pb208":
                    continue

                if Comparison == "NuclearRatio_RelativeUncertainty" and any(ext in Setname for ext in N1s) and Setname != "EPPS16nlo_CT14nlo_Pb208":
                    continue

                ##
                if fl == LegendPosition:
                    label_suffix=""
                    if iSet == Ratio_den_Set and Comparison == "Ratio":
                        label_suffix=r" {\rm [ref]}"

                    p1 = axs[ifl].plot(X, Y, color=color, ls=ls, lw=1.5)
                    p1s.append(p1[0])

                    if Comparison == "NuclearRatio" or Comparison == "NuclearRatio_pull" or Comparison == "NuclearRatio_RelativeUncertainty":
                        LABEL = Setlabels[int((iSet+1)/2)-1]+label_suffix
                    else:
                        LABEL = Setlabels[iSet]+label_suffix

                    if Comparison != "Relative Uncertainty":
                        if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                            axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=color, edgecolor=color, alpha=0.25, lw=0.1) #, label=LABEL)
                            p2 = axs[ifl].fill(np.NaN, np.NaN, facecolor=color, edgecolor=color, alpha=0.25, lw=0.1)
                            #p2s.append(p2)
                            ps.append((p2[0], p1[0]))
                    
                    labels.append(LABEL)
                    #lg = axs[ifl].legend(ps,labels,loc='best', title=r'{\rm \textbf{'+NUCLEUS+r'} \textbf{'+PTO+r'} ($Q=' + '{: .1f}'.format(
                    #    Q)+r'\, \, {\rm GeV}$)\\}', # \textbf{[Preliminary]}\\}',
                    #     fontsize=legend_fontsize, ncol=1, frameon=False, handletextpad=-1.8)
                    #lg.get_title().set_fontsize(fontsize=legend_fontsize)

                else:
                    axs[ifl].plot(X, Y, color=color, ls=ls, lw=1.5)
                    if Comparison != "Relative Uncertainty":
                        if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                            axs[ifl].fill_between(X, Y_plus, Y_minus, facecolor=color, edgecolor=color, alpha=0.25, lw=0.1)

                if Comparison == "AbsolutesandRatio":
                    axs2[ifl].plot(X, Y2, color=color, ls=ls2, lw=1.5)
                    axs2[ifl].fill_between(X, Y2_plus, Y2_minus, facecolor=color, edgecolor=color, alpha=0.25, lw=0.1)

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

                    ##!temp

                if Comparison == "NuclearRatio":
                    axs[ifl].axhline(y=1, linewidth=1.5, ls='--', color='k')
                    


                if Comparison == "NuclearRatio_pull":
                    axs[ifl].axhline(y=0, linewidth=1.5, ls='--', color='k')
                    axs[ifl].axhline(y=-3, linewidth=1.5, ls='dotted', color='r')
                    if fl == 'g': axs[ifl].axhline(y=+3, linewidth=1.5, ls='dotted', color='g')
                    
                ##
                if not ifl%ncol:
                    axs[ifl].set_ylabel(r'{\rm \boldmath'+dist+'}', fontsize=fontsize, rotation=90)
                    axs[ifl].yaxis.set_label_coords(-0.09, 0.5)
                    if Comparison == "AbsolutesandRatio":
                        axs2[ifl].set_ylabel(r'{\rm \textbf{'+dist2+'}}', fontsize=fontsize, rotation=90)
                        axs2[ifl].yaxis.set_label_coords(-0.09, 0.5)
                
                fl_label_scale=1
                if fl == 'u^+ + d^+ + s^+':
                    fl_label_scale=2.75
                axs[ifl].text(0.075*fl_label_scale, 0.9, r'{\rm \boldmath $'+fl+'$}' , horizontalalignment='center', verticalalignment='center', transform=axs[ifl].transAxes, fontsize=fontsize)

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

        #ps = []
        #labels = []
        #for iSet, Setname in enumerate(Setsnames):
        #    ps.append((p2s[iSet][0], p1s[iSet][0]))
        #    labels.append(LABEL)

        if UNCERTAINTY == "68CL":
            #LABEL = r'{\rm {\large $~^{68\%~{\rm CL}}$} ~~' + Setlabels[iSet]+label_suffix
            UNCLABEL =  [r'{\rm median}', r'{\rm 68\% CL}']
        elif UNCERTAINTY == "90CL":
            #LABEL = r'{\rm {\large $~^{68\%~{\rm CL}}$} ~~' + Setlabels[iSet]+label_suffix
            UNCLABEL =  [r'{\rm median}', r'{\rm 90\% CL}']
        elif UNCERTAINTY == "std":
            #LABEL = r'{\rm {\large $~^{\pm~\sigma}$} ~~~~~' + Setlabels[iSet]+label_suffix
            UNCLABEL =  [r'{\rm mean}', r'$\pm \sigma$']

        if Comparison != "Relative Uncertainty" and Comparison != "NuclearRatio_pull" and Comparison != "NuclearRatio_RelativeUncertainty":
            if comparison_choice != "PRL_therr" or Setname != "NNPDF31_nnlo_as_0118_kF_1_kR_1":
                for ifl, fl in enumerate(flavors_to_plot):
                    if fl == LegendPosition:
                        lg = axs[ifl].legend(ps,labels,loc=PDFlabel_loc, title=r'{\rm \textbf{'+NUCLEUS+r'} \textbf{'+PTO+r'}\\}', # \textbf{[Preliminary]}\\}',
                                fontsize=legend_fontsize, ncol=1, frameon=False)#, handletextpad=-1.8)
                        lg.get_title().set_fontsize(fontsize=legend_fontsize)

                        if ncol==2:
                            adjacent_ifl=1
                        elif ncol==3:
                            adjacent_ifl=3

                        axs[ifl+adjacent_ifl].plot(np.NaN, np.NaN, color='black', ls=ls, lw=1.5,label=UNCLABEL[0])
                        axs[ifl+adjacent_ifl].fill(np.NaN, np.NaN, facecolor='black', edgecolor='black', alpha=0.25, lw=0.1,label=UNCLABEL[1])
                        lg2 = axs[ifl+adjacent_ifl].legend(loc=Settingslabel_loc, title=r'{\rm $Q=' + '{: .1f}'.format(
                            Q)+r'\, \, {\rm GeV}$\\}',  # \textbf{[Preliminary]}\\}',
                                fontsize=legend_fontsize, ncol=1, frameon=False)
                        #lg2 = axs[ifl+adjacent_ifl].legend([],[],loc='upper right', title=r'{\rm $Q=' + '{: .1f}'.format(
                        #    Q)+r'\, \, {\rm GeV}$\\'+UNCLABEL+r'}',  # \textbf{[Preliminary]}\\}',
                        #        fontsize=legend_fontsize, ncol=1, frameon=False, handletextpad=-1.8)
                        lg2.get_title().set_fontsize(fontsize=legend_fontsize)
        else:
            for ifl, fl in enumerate(flavors_to_plot):
                if fl == LegendPosition:
                    lg = axs[ifl].legend(p1s, labels, loc=PDFlabel_loc, title=r'{\rm \textbf{'+NUCLEUS+r'} \textbf{'+PTO+r'} ($Q=' + '{: .1f}'.format(
                        Q)+r'\, \, {\rm GeV}$)\\}', # \textbf{[Preliminary]}\\}',
                        fontsize=legend_fontsize, ncol=1, frameon=False)
                    lg.get_title().set_fontsize(fontsize=legend_fontsize)

        py.tight_layout()
        py.savefig(outputname+'/'+comparison_choice+'_'+Comparison.split(" ")[0] +
                Type_of_sets+'_Q'+str(int(Q))+output_format)

        py.clf()
        py.cla()

    print("------")
