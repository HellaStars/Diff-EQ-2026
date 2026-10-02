#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:00:26 2026

@author: Asta Walor-Scott
@email:lwalorsc@msudenver.edu
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# Equation 1
def eq1(x, t, r): 
    return r + (x**2)

# Equation 2
def eq2(x, t, r): 
    return r - (x**2)

# Equation 3
def eq3(x, t, r):
    return (r * x) - (x**3)

# Equation 4
def eq4(x, t, r):
    return (r * x) + (x**3)
    
# Equation 5
def eq5(x, t, c, d):
    return d + (c * x) - (x**3)

t = np.linspace(0, 5, 100)
x0 = [-3, -2.5, -2, -1.5, -1, -.5, 0, .5, 1, 1.5, 2, 2.5, 3, 3.5] #half values added for additional info
rval = [-4, -1, 0, 1]

eq = [eq1, eq2, eq3, eq4]

#equation 5 requres additional values
dval = [1, 4, -1, -4]
cval = [-4, -1, 0, 1, 1.8, 1.9, 2.5] #2.5 added for more into

save_dir = "/home/deck/Desktop/School/diffEQ/Plots"
os.makedirs(save_dir, exist_ok=True) 

for ceq in eq:
    for r in rval:
        plt.figure()
        
        for xf in x0:
            solution = odeint(ceq, xf, t, args=(r,))
            bp = np.where(np.abs(solution) > 10)[0] 
            
            if len(bp) > 0:
                first_blowup = bp[0]
                solution[first_blowup:] = np.nan 
                
            plt.plot(t, solution, label=f"xf={xf}")
            
        plt.xlabel("Time (t)")
        plt.ylabel("x(t)")
        plt.title(f"Solutions for {ceq.__name__} with r={r}")
        plt.ylim(-5, 5)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid()
        
        # Equilibrium line logic (Restricted to eq2 for now)
        if ceq == eq2 and r >= 0:
            eq_val = np.sqrt(r)
            plt.axhline(y=eq_val, color="#800080", linestyle='--')
            if r > 0:
                plt.axhline(y=-eq_val, color="#0000FF", linestyle='--')
                
        filename = f"{save_dir}/{ceq.__name__}_r_{r}.png"
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
#eqn 5 special
for d in dval:
    for c in cval:
        plt.figure()
        
        for xf in x0:
            solution = odeint(eq5, xf, t, args=(c, d))
            bp = np.where(np.abs(solution) > 10)[0] 
            
            if len(bp) > 0:
                first_blowup = bp[0]
                solution[first_blowup:] = np.nan 
                
            plt.plot(t, solution, label=f"xf={xf}")
            
        plt.xlabel("Time (t)")
        plt.ylabel("x(t)")
        plt.title(f"Solutions for Eq5 with c={c}, d={d}")
        plt.ylim(-5, 5)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid()
        
        filename = f"{save_dir}/Eq5_d_{d}_c_{c}.png"
        plt.savefig(filename, bbox_inches='tight')
        plt.close()        

# eq5 moving bifircation plots
cval_bf = np.linspace(-4, 5, 1000)

for d in dval:
    plt.figure(figsize=(8, 6))
    
    for c in cval_bf:
        roots = np.roots([-1, 0, c, d])
        for root in roots:
            if np.isreal(root):
                r = np.real(root)
                if c - 3*(r**2) < 0:
                    plt.plot(c, r, 'b.', markersize=2)  
                else:
                    plt.plot(c, r, 'r.', markersize=2)  
                    
    plt.xlabel("Parameter c")
    plt.ylabel("Equilibrium x*")
    plt.title(f"Bifurcation Diagram for Eq 5 (d={d})")
    plt.grid()
    
    # Using plt.plot to create empty proxy artists for the legend instead of mlines
    stable_line, = plt.plot([], [], color='blue', marker='.', linestyle='None', label='Stable Equilibrium')
    unstable_line, = plt.plot([], [], color='red', marker='.', linestyle='None', label='Unstable Equilibrium')
    plt.legend(handles=[stable_line, unstable_line])
    
    filename = f"{save_dir}/Bifurcation_Eq5_d_{d}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()    
