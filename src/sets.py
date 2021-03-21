import collections
import yaml
import lhapdf
cfg = lhapdf.getConfig()
cfg.set_entry("Verbosity", 0)
import numpy as np
import sys
import os
sys.path.append(os.getcwd()+"/../")

evlfl = {r'$\gamma$': 0, r'$\Sigma$': 1, r'$g$': 2, r'$V$': 3, r'$V_3$': 4, r'$V_8$': 5, r'$V_{15}$': 6,
         r'$V_{24}$': 7, r'$V_{35}$': 8, r'$T_{3}$': 9, r'$T_{3}$': 10, r'$T_{15}$': 11, r'$T_{24}$': 12, r'$T_{35}$': 13}

lhafl = {r'$\bar{t}$': 0, r'$\bar{b}$': 1, r'$\bar{c}$': 2, r'$\bar{s}$': 3, r'$\bar{u}$': 4, r'$\bar{d}$': 5,
         r'$g$': 6, r'$d$': 7, r'$u$': 8, r'$s$': 9, r'$c$': 10, r'$b$': 11, r'$t$': 12, r'$\gamma$': 13}

rev_evlfl = {}
rev_lhafl = {}

#reversing dictionaries
for key, value in evlfl.items():
    rev_evlfl[value] = key

for key, value in lhafl.items():
    rev_lhafl[value] = key

def LHA2EVLN(LHA):

    uplus = LHA[lhafl[r'$u$']] + LHA[lhafl[r'$\bar{u}$']]
    uminus = LHA[lhafl[r'$u$']] - LHA[lhafl[r'$\bar{u}$']]

    dplus = LHA[lhafl[r'$d$']] + LHA[lhafl[r'$\bar{d}$']]
    dminus = LHA[lhafl[r'$d$']] - LHA[lhafl[r'$\bar{d}$']]

    cplus = LHA[lhafl[r'$c$']] + LHA[lhafl[r'$\bar{c}$']]
    cminus = LHA[lhafl[r'$c$']] - LHA[lhafl[r'$\bar{c}$']]

    splus = LHA[lhafl[r'$s$']] + LHA[lhafl[r'$\bar{s}$']]
    sminus = LHA[lhafl[r'$s$']] - LHA[lhafl[r'$\bar{s}$']]

    tplus = LHA[lhafl[r'$t$']] + LHA[lhafl[r'$\bar{t}$']]
    tminus = LHA[lhafl[r'$t$']] - LHA[lhafl[r'$\bar{t}$']]

    bplus = LHA[lhafl[r'$b$']] + LHA[lhafl[r'$\bar{b}$']]
    bminus = LHA[lhafl[r'$b$']] - LHA[lhafl[r'$\bar{b}$']]

    EVL = np.zeros(14)
    EVL[evlfl[r'$\gamma$']] = LHA[lhafl[r'$\gamma$']]  # photon
    EVL[evlfl[r'$\Sigma$']] = (uplus + dplus + cplus +
                            splus + tplus + bplus)  # Singlet
    EVL[evlfl[r'$g$']] = (LHA[lhafl[r'$g$']])  # Gluon

    EVL[evlfl[r'$V$']] = (uminus + dminus + sminus +
                        cminus + bminus + tminus)  # V
    EVL[evlfl[r'$V_3$']] = (uminus - dminus)  # V3
    EVL[evlfl[r'$V_8$']] = (uminus + dminus - 2 * sminus)  # V8
    EVL[evlfl[r'$V_{15}$']] = (uminus + dminus + sminus - 3 * cminus)  # V15
    EVL[evlfl[r'$V_{24}$']] = (uminus + dminus + sminus +
                            cminus - 4 * bminus)  # V24
    EVL[evlfl[r'$V_{35}$']] = (uminus + dminus + sminus +
                            cminus + bminus - 5 * tminus)  # V35

    EVL[evlfl[r'$T_{3}$']] = (uplus - dplus)  # T3
    EVL[evlfl[r'$T_{3}$']] = (uplus + dplus - 2 * splus)  # T8
    EVL[evlfl[r'$T_{15}$']] = (uplus + dplus + splus - 3 * cplus)  # T15
    EVL[evlfl[r'$T_{24}$']] = (uplus + dplus + splus + cplus - 4 * bplus)  # T24
    EVL[evlfl[r'$T_{35}$']] = (uplus + dplus + splus +
                            cplus + bplus - 5 * tplus)  # T35

    return EVL

def Get(setname, X, q, Replicas):
    SETs = {}
    for Replica in range(0,Replicas):
        # initialization
        LHAPDF = lhapdf.mkPDF(setname, Replica)

        if q == 0:
            q = np.sqrt(LHAPDF.q2Min)

        SET={}

        for fl in rev_evlfl.values():
            SET[fl] = []

        for fl in rev_lhafl.values():
            if fl == r'$g$' or fl == r'$\gamma$':
                continue
            SET[fl] = []

        for j in range(X.size):
            LHA = {}
            x = X[j]

            for fl in range(-6, 8):
                LHA[fl+6] = LHAPDF.xfxQ(fl, x, q)
                if rev_lhafl[fl+6] != r'$g$' and rev_lhafl[fl+6] != r'$\gamma$':
                    SET[rev_lhafl[fl+6]].append(LHA[fl+6])
            
            EVL = LHA2EVLN(LHA)

            for ifl, fl in rev_evlfl.items():
                SET[fl].append(EVL[ifl])

        for fl in rev_evlfl.values():
            SET[fl] = np.array(SET[fl])
        for fl in rev_lhafl.values():
            if fl != r'$g$' and fl != r'$\gamma$':
                SET[fl] = np.array(SET[fl])

        #combinations
        SET[r'$F_2^{LO}$'] = SET[r'$\Sigma$']+(1./4)*SET[r'$T_{3}$']
        SET[r'$u^+$'] = SET[r'$u$']+SET[r'$\bar{u}$']
        SET[r'$d^+$'] = SET[r'$d$']+SET[r'$\bar{d}$']
        SET[r'$s^+$'] = SET[r'$s$']+SET[r'$\bar{s}$']
        SET[r'$c^+$'] = SET[r'$c$']+SET[r'$\bar{c}$']
        SET[r'$b^+$'] = SET[r'$b$']+SET[r'$\bar{b}$']
        SET[r'$t^+$'] = SET[r'$t$']+SET[r'$\bar{t}$']

        SET[r'$u^-$'] = SET[r'$u$']-SET[r'$\bar{u}$']
        SET[r'$d^-$'] = SET[r'$d$']-SET[r'$\bar{d}$']
        SET[r'$s^-$'] = SET[r'$s$']-SET[r'$\bar{s}$']
        SET[r'$c^-$'] = SET[r'$c$']-SET[r'$\bar{c}$']
        SET[r'$b^-$'] = SET[r'$b$']-SET[r'$\bar{b}$']
        SET[r'$t^-$'] = SET[r'$t$']-SET[r'$\bar{t}$']

        for fl in SET.keys():
            if Replica == 0:
                SETs[fl]=[]

            SETs[fl].append(SET[fl])


    for fl in SETs.keys():
        SETs[fl] = np.array(SETs[fl])
        
    return SETs


def GetStats(SETs, Error_type):
    #See https://arxiv.org/Set/1412.7420.pdf for error type definitions

    flavors = list(SETs.keys()) #shallow copy

    SETs["low"] = {}
    SETs["up"] = {}
    SETs["median"] = {}
    SETs["std"] = {}
    SETs["mean"] = {}

    for fl in flavors:
        Nmem = SETs[fl].shape[0]
        Nx = SETs[fl].shape[1]

        if Error_type == "MC":
            SETs["low"][fl] = np.nanpercentile(SETs[fl][1:Nmem, :], 5., axis=0)
            SETs["up"][fl] = np.nanpercentile(SETs[fl][1:Nmem, :], 95., axis=0)
            SETs["median"][fl] = np.median(SETs[fl][1:Nmem,:], axis=0)
            SETs["mean"][fl] = SETs[fl][0, :]
            SETs["std"][fl] = np.std(SETs[fl][1:Nmem,:], axis=0)
            
        elif Error_type == "hessian":
            SETs["mean"][fl] = SETs[fl][0, :]
            SETs["std"][fl] = np.zeros(Nx)
            for im in range(0, int((Nmem-1)/2)):
                fp = SETs[fl][2*im+1, :]
                fm = SETs[fl][2*im+2, :]
                SETs["std"][fl] += (fp-fm)**2
            SETs["std"][fl] = np.sqrt(SETs["std"][fl])/2

        elif Error_type == "symmhessian":
            SETs["mean"][fl] = SETs[fl][0, :]
            SETs["std"][fl] = np.zeros(Nx)
            for im in range(1, Nmem):
                f = SETs[fl][im, :]
                SETs["std"][fl] += (f-SETs["mean"][fl] )**2
            SETs["std"][fl] = np.sqrt(SETs["std"][fl])

    return SETs
