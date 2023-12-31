# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 13:27:35 2023

@author: user
"""

import numpy as np
import argparse
import mtanh_fitting as mf
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

parser = argparse.ArgumentParser(description='load MAST data file')
parser.add_argument('-d','--mastfile_loc', type=str, default=None, help='location MAST data file')
args = parser.parse_args()

def read_mastfile(mastfile_loc):
    with open(mastfile_loc, mode='r') as dfile:
        lines = dfile.readlines()
    
    profiles = {}
    nlines_tot = len(lines)
    psi_n = np.zeros(nlines_tot)
    ne = np.zeros(nlines_tot)
    te = np.zeros(nlines_tot)
    i = 0
    
    while i < nlines_tot:
        r_line = lines[i].split()
        psi_n[i] = float(r_line[0])
        ne[i] = float(r_line[1])*pow(10, -20)
        te[i] = float(r_line[3])/1000
        i += 1

    profiles['psi_normal'] = psi_n
    profiles['electron_density(10^20/m^3)'] = ne
    profiles['electron_temperature(KeV)'] = te
    return profiles

if __name__ == '__main__':
    n_tot = 200
    mast_dat_dict = read_mastfile(args.mastfile_loc)
    psi = mast_dat_dict['psi_normal']
    size = len(psi)
    ne = mast_dat_dict['electron_density(10^20/m^3)']
    te = mast_dat_dict['electron_temperature(KeV)']
    
    
    ne_f = interp1d(psi, ne, kind= 'linear')
    te_f = interp1d(psi, te, kind= 'quadratic')
    
    x_model = np.linspace(min(psi), max(psi), n_tot)
    
    
    # ne_fit = mf.super_fit_osbourne(psi, ne)
    # ne_superfit = mf.best_osbourne(psi, ne)
    
    # te_fit = mf.super_fit_osbourne(psi, te)
    # te_superfit = mf.best_osbourne(psi, te)
    
    ne_pop = mf.super_fit_osbourne(x_model, ne_f(x_model))
    ne_superpop = mf.best_osbourne(x_model, ne_f(x_model))
    
    te_pop = mf.super_fit_osbourne(x_model, te_f(x_model))
    te_superpop = mf.best_osbourne(x_model, te_f(x_model))
    
    ne_plat = np.zeros(178)
    x_plat = np.zeros(178)
    for j in range(178):
        ne_plat[j] = ne_pop[0][j]
        x_plat[j] = x_model[j]
    
    
    gnexp = np.gradient(ne_plat) / (np.gradient(x_plat))
    gne = np.gradient(ne_pop[0]) / (np.gradient(x_model))
    
    
    # plt.figure(1)
    # plt.plot(psi, ne_fit[0], color='r', label= 'electron density fit')
    # plt.plot(psi, ne_superfit[0], color='r', label= 'electron density fit')
    # plt.scatter(psi, ne, label= 'electron density experiment data')
    
    # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    # plt.ylabel('Electron density: ${n_e}$ (m$^{-3}$)', fontdict={"family":"Times New Roman","size": 20})
    # plt.title('Electron density',fontdict={"family":"Times New Roman","size": 20})
    # plt.legend()
    
    
    
    # plt.figure(2)
    # plt.plot(psi, te_fit[0], color='r', label= 'electron density fit')
    # plt.plot(psi, te_superfit[0], color='r', label= 'electron density fit')
    # plt.scatter(psi, te, label= 'electron density experiment data')
    
    # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    # plt.ylabel('Electron temperature: ${T_e}$ (eV)', fontdict={"family":"Times New Roman","size": 20})
    # plt.title('Electron temperature',fontdict={"family":"Times New Roman","size": 20})
    # plt.legend()
    
    
    plt.figure(1)
    plt.plot(x_model, ne_pop[0], color='r', label= 'electron density fit')
    plt.plot(x_model, ne_superpop[0], color='g', label= 'electron density super fit')
    plt.scatter(psi, ne, label= 'electron density experiment data')
    
    plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    plt.ylabel('Electron density: ${n_e}$ (m$^{-3}$)', fontdict={"family":"Times New Roman","size": 20})
    plt.title('Electron density',fontdict={"family":"Times New Roman","size": 20})
    plt.legend()
    
    
    
    plt.figure(2)
    plt.plot(x_model, te_pop[0], color='r', label= 'electron temperature fit')
    plt.plot(x_model, te_superpop[0], color='g', label= 'electron temperature super fit')
    plt.scatter(psi, te, label= 'electron temperature experiment data')
    
    plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    plt.ylabel('Electron temperature: ${T_e}$ (eV)', fontdict={"family":"Times New Roman","size": 20})
    plt.title('Electron temperature',fontdict={"family":"Times New Roman","size": 20})
    plt.legend()
    
    # plt.figure(3)
    # plt.plot(x_plat, gnexp, color='r', label= 'gradiant')
    
    # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    # plt.ylabel('Electron density gradiant', fontdict={"family":"Times New Roman","size": 20})
    # plt.title('Electron density gradiant',fontdict={"family":"Times New Roman","size": 20})
    # plt.legend()
    
    # plt.figure(4)
    # plt.plot(x_model, gne, color='r', label= 'gradiant')
    
    # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$', fontdict={"family":"Times New Roman","size": 20})
    # plt.ylabel('Electron density gradiant', fontdict={"family":"Times New Roman","size": 20})
    # plt.title('Electron density gradiant',fontdict={"family":"Times New Roman","size": 20})
    # plt.legend()
    
    plt.show()
    
    # w_datalist = []   
    # for j in range(size):
    #     w_list =[]
    #     w_list.append("{: .6f}".format(psi[j]))
    #     w_list.append("{: .6f}".format(ne_fit[0][j]))
    #     w_list.append("{: .6f}".format(te_fit[0][j]))
    #     w_writelist = ' '.join(str(y)+ "\t" for y in w_list)
    #     w_datalist.append(w_writelist)
   
    # with open('fit_27205_275.dat', 'w') as f:
    #     for l,w_line in enumerate(w_datalist):   
    #         f.writelines(w_line + "\n")
            
    # w_datalist = []   
    # for k in range(n_tot):
    #     w_list =[]
    #     w_list.append("{: .6f}".format(x_model[k]))
    #     w_list.append("{: .6f}".format(ne_pop[0][k]))
    #     w_list.append("{: .6f}".format(te_pop[0][k]))
    #     w_writelist = ' '.join(str(y)+ "\t" for y in w_list)
    #     w_datalist.append(w_writelist)
   
    # with open('fit_pop_27205_275.dat', 'w') as f:
    #     for l,w_line in enumerate(w_datalist):   
    #         f.writelines(w_line + "\n")

    
    