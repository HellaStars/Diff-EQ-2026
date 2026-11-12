#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:31:13 2026

@author: HellaStars
@Email:lwalorsc@msudenver.edu
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Clear previous figures and ensure directory exists
if os.path.exists('Plots'): #actually removing the plots so I don't have a billion plots :)
    shutil.rmtree('Plots')
os.makedirs('Plots') #dir


# ==========================================
# PART 1: ORIGINAL SIMIODE PARAMETERS (Q1 - Q5)
#I wasn't sure what was exactly wanted........ So i'm doing both. I'm sorry
# Equation: x'' + 2x' + 16x = 3sin(wt)
# ==========================================

def simiode_undamped(y, t, omega):
    return [y[1], -16.0 * y[0] + 3.0 * np.sin(omega * t)]

def simiode_damped(y, t, omega):
    return [y[1], -16.0 * y[0] - 2.0 * y[1] + 3.0 * np.sin(omega * t)]

t_sim = np.linspace(0, 20, 1000)

# Questions 1, 2, 3: Undamped plots
for w in [8, 5, 4]:
    sol = odeint(simiode_undamped, [0.0, 0.0], t_sim, args=(w,))
    
    plt.figure(figsize=(8, 4)) #all the basic plotting stuff
    plt.plot(t_sim, sol[:, 0], color='tab:blue') 
    plt.title(f'SIMIODE Undamped: Driving Frequency ω = {w}')
    plt.xlabel('Time (t)')
    plt.ylabel('Displacement (x)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Plots/simiode_undamped_w{w}.png', dpi=300)
    plt.close()

# Question 4: Damped plots comparing frequencies
#Lots of intigrations of ODE's
sol_a = odeint(simiode_damped, [0.0, 0.0], t_sim, args=(8,))
sol_b = odeint(simiode_damped, [0.0, 0.0], t_sim, args=(4,))
#so much plotting
plt.figure(figsize=(8, 4))
plt.plot(t_sim, sol_a[:,0], label='(a) ω=8, Init=[0,0]', color='tab:blue')
plt.plot(t_sim, sol_b[:,0], label='(b) ω=4, Init=[0,0]', color='tab:red')
plt.title('SIMIODE Damped: Non-Resonant vs Resonant')
plt.xlabel('Time (t)')
plt.ylabel('Displacement (x)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots/simiode_damped_ab.png', dpi=300)
plt.close()

# Question 4 & 5: Damped plots comparing initial conditions
#more intigration
sol_c = odeint(simiode_damped, [0.0, 5.0], t_sim, args=(4,))
sol_d = odeint(simiode_damped, [1.0, 0.0], t_sim, args=(4,))

#more plotting
plt.figure(figsize=(8, 4))
plt.plot(t_sim, sol_b[:,0], label='(b) Init Disp: 0, Vel: 0', color='tab:red')
plt.plot(t_sim, sol_c[:,0], label='(c) Init Disp: 0, Vel: 5', color='tab:green', linestyle='-.')
plt.plot(t_sim, sol_d[:,0], label='(d) Init Disp: 1, Vel: 0', color='tab:purple', linestyle=':')
plt.title('SIMIODE Damped (ω=4): Effect of Initial Conditions')
plt.xlabel('Time (t)')
plt.ylabel('Displacement (x)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots/simiode_damped_bcd.png', dpi=300)
plt.close()


# ==========================================
# QUESTION 6 CALCULATIONS
#given by simiode
# ==========================================

k_m = 16.0  
b_m = 2.0   
F0_m = 3.0  

w_prac = np.sqrt(k_m - (b_m**2)/2.0)
A_prac = F0_m / np.sqrt((k_m - w_prac**2)**2 + (b_m*w_prac)**2)

print("--- Question 6: SIMIODE Calculations ---")
print(f"Practical Resonance Frequency (w): {w_prac:.4f}")
print(f"Largest Steady-State Amplitude (A): {A_prac:.4f}\n")


# ==========================================
# PART 2: TESLA MACHINE ("Have child like wonder" WELL AS A CHILD I WAS OBSESSED WITH TESLA!)
# ==========================================

t_tesla = np.linspace(0, 20, 1000) #tesla time (sounds scifi)

# --- Q1-Q3: Undamped (Tesla Lab Pillar) ---
M_lab = 5000.0 #weight of a steel beam (High end)
K_lab = 16.0 * M_lab  # Maintains w0 = 4 from simiode (pretty much 4 times larger)
F0_lab = 500.0

def lab_undamped(y, t, omega):
    return [y[1], -(K_lab/M_lab)*y[0] + (F0_lab/M_lab)*np.sin(omega * t)]

for w in [8, 5, 4]:
    #intigration
    sol = odeint(lab_undamped, [0.0, 0.0], t_tesla, args=(w,))
    #plotting
    plt.figure(figsize=(8, 4))
    plt.plot(t_tesla, sol[:,0], color='black')
    plt.title(f'Tesla Lab Pillar: Undamped Response (ω = {w})')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (m)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Plots/tesla_lab_undamped_w{w}.png', dpi=300)
    plt.close()

# --- Q4-Q5: Damped (Empire State Building) ---
M_esb = 331122430.0 #weight of the empire state building
K_esb = 16.0 * M_esb  #again to maintain w=4
B_esb = 2.0 * M_esb   
F0_esb = 500.0

def esb_damped(y, t, omega):
    return [y[1], -(K_esb/M_esb)*y[0] - (B_esb/M_esb)*y[1] + (F0_esb/M_esb)*np.sin(omega * t)]

# Q4: Frequencies Intigration
sol_esb_a = odeint(esb_damped, [0.0, 0.0], t_tesla, args=(8,))
sol_esb_b = odeint(esb_damped, [0.0, 0.0], t_tesla, args=(4,))
#plotting
plt.figure(figsize=(8, 4))
plt.plot(t_tesla, sol_esb_a[:,0], label='(a) Non-Resonant (ω=8)', color='tab:blue')
plt.plot(t_tesla, sol_esb_b[:,0], label='(b) Resonant (ω=4)', color='tab:red')
plt.title('Empire State Building: Frequency Comparison')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots/tesla_esb_damped_freq.png', dpi=300)
plt.close()

# Q4 & Q5: Initial Conditions 
sol_esb_c = odeint(esb_damped, [0.0, 5.0], t_tesla, args=(4,))
sol_esb_d = odeint(esb_damped, [1.0, 0.0], t_tesla, args=(4,))

plt.figure(figsize=(8, 4))
plt.plot(t_tesla, sol_esb_b[:,0], label='Start at Rest', color='tab:red')
plt.plot(t_tesla, sol_esb_c[:,0], label='Initial Velocity (5 m/s)', color='tab:green', linestyle='-.')
plt.plot(t_tesla, sol_esb_d[:,0], label='Initial Displacement (1 m)', color='tab:purple', linestyle=':')
plt.title('Empire State Building (ω=4): Convergence to Steady-State')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')

plt.yscale('symlog', linthresh=1e-5)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots/tesla_esb_initial_cond.png', dpi=300)
plt.close()

# --- Q6: Practical Resonance Calculation (ESB) ---
w_esb_prac = np.sqrt((K_esb/M_esb) - (B_esb/M_esb)**2 / 2.0)
A_esb_prac = (F0_esb/M_esb) / np.sqrt(((K_esb/M_esb) - w_esb_prac**2)**2 + ((B_esb/M_esb)*w_esb_prac)**2)

print("--- Tesla Historical Parameter Calculations ---")
print(f"ESB Practical Resonance Frequency (w): {w_esb_prac:.4f} rad/s")
print(f"ESB Largest Steady-State Amplitude (A): {A_esb_prac:.4e} m\n")