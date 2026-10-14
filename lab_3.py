import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

df = pd.read_csv('data.csv')

time = df['Time_s']
pot_reading = df['Potentiometer']
therm_reading = df['ThermistorRaw']

temp = 0
duty_cycle = 100* pot_reading/1023

#find the temp
T_25 = 298.15
R_25 = 3300
B = 2.569850 / 10000
C = 2.620131 / 1000000
D = 6.383091 / 100000000
R0 = 1000

def find_temp(therm_reading):
    R_T = R0 * ((1023-therm_reading)/therm_reading)
    temp = 1/((1/T_25) + ((B) * np.log(R_T/R_25))) + (C * (np.log(R_T/R_25)**2)) + (D * (np.log(R_T/R_25)**3))

    return temp

temp = find_temp(therm_reading) - 273.15

#####################FIGURES####################
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 8), sharex=True)

#top plot
ax1.plot(time, duty_cycle)
ax1.set_ylabel('Duty Cycle (%)')
ax1.set_title('Potentiometer Cycle vs. Time')
ax1.grid(True, linestyle='--', alpha=0.5)

#bottom plot
ax2.scatter(time, temp, s=1)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Temperature (C)')
ax2.set_title('Thermistor Reading vs. Time')
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("my_plot1.pdf", bbox_inches="tight")
plt.show()


#cooling fit
truncated = df[484:]
time_trunc = truncated['Time_s']
temp_trunc = temp[484:]

def fit_curve(t, del_T, tau, T_env):
    return del_T * np.exp(-t/tau) + T_env

initial_T_env = 25                      
initial_del_T = temp_trunc.iloc[0] - initial_T_env       
initial_tau = (time_trunc.iloc[-1] - time_trunc.iloc[0]) / 3  #using rule of 3s

guesses = [initial_del_T, initial_tau, initial_T_env]

popt, pcov = curve_fit(fit_curve, time_trunc, temp_trunc, p0=guesses)
del_T_opt, tau_opt, T_env_opt = popt

y_fit = fit_curve(time_trunc, del_T_opt, tau_opt, T_env_opt)

plt.scatter(time_trunc, temp_trunc, s=1, label="Cooling Curve, Time > 97.67s")
plt.scatter(time_trunc, y_fit, s=1, label=fr"$Best\ Fit\ Curve:\ \tau={popt[1]:.2f}\ s$")
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.legend()
plt.savefig("my_plot2.pdf", bbox_inches="tight")
plt.show()

