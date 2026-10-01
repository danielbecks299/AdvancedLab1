import serial
import matplotlib.pyplot as plt
import numpy as np

arduino = serial.Serial("/dev/cu.usbmodem1101", 9600)

time_array = []
v_out_array = []
v_in = 5.0

def find_resist(R1, v_in, v_out):
    return R1 * ((v_in / v_out) - 1)

for i in range(450):
    line = arduino.readline().decode().strip()
    times, v_out = map(float, line.split())

    time_array.append(times)
    v_out_array.append(v_out)

arduino.close()

# Convert lists to NumPy arrays for element-wise math
time_array = np.array(time_array)
v_out_array = np.array(v_out_array)

# Calculate Thermistor Resistance
R_1 = 1000  # Fixed resistor (1k ohm)
R_T = find_resist(R_1, v_in, v_out_array)

def find_temp(T0, R_T, beta, R_0):
    inv_T = (1/T0) + (1/beta) * np.log(R_T/R_0)
    return (1/inv_T)

T0 = 298.15 #room temp
beta = 3977
R_0 = 3300 #resistance of thermoresistor at 25C

T = find_temp(T0, R_T, beta, R_0)

plt.figure(figsize=(8, 5))
plt.plot(time_array, T)

plt.xlabel(r"$Time, ms$")
plt.ylabel(r"$Temperature, K$")
plt.legend(title=r'Temperature of Resistor vs. Time')

plt.savefig("voltage_divider_plot.pdf")

plt.show()