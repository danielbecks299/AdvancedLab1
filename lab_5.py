import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd

# arduino = serial.Serial("/dev/cu.usbmodem1101", 1000000)

# time.sleep(1)
# arduino.reset_input_buffer()

# time_array = [0]
# A0_array = [0]

# while time_array[-1] < 100:
#     line = arduino.readline().decode().strip()
#     if line:  # Ensure line isn't empty
#         try:
#             times, A0 = map(float, line.split(","))
#             time_array.append(times)
#             A0_array.append(A0)
#         except ValueError:
#             continue  # Skip any malformed print lines

# arduino.close()

# time_array.pop(0)
# A0_array.pop(0)

# raw_signal = np.array(A0_array, dtype=float)
# voltage_signal = raw_signal * (5.0 / 1023.0)

# df = pd.DataFrame({
#     "Time_ms": time_array,
#     "Voltage_V": voltage_signal
# })

# # 2. Save to CSV (index=False prevents saving the row numbers)
# df.to_csv('f60Hz.csv', index=False)

df1 = pd.read_csv('unf60Hz.csv')
df2 = pd.read_csv('f60Hz.csv')

time_data = df1['Time_ms']
unf_voltage_data = df1['Voltage_V']
filt_voltage_data = df2['Voltage_V']

#PLOTS
plt.plot(time_data, unf_voltage_data, label="Unfiltered")
plt.plot(time_data, filt_voltage_data, label = "Filtered")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage")
plt.title("PWM Output Capture for 60Hz Square Wave")
plt.legend()

plt.savefig('voltage_plot.pdf', format='pdf', bbox_inches='tight')

plt.show()

#to build bode plot
df20 = pd.read_csv('f20Hz.csv')
df40 = pd.read_csv('f20Hz.csv')
df50 = pd.read_csv('f50Hz.csv')
df60 = pd.read_csv('f60Hz.csv')
df70 = pd.read_csv('f70Hz.csv')
df80 = pd.read_csv('f80Hz.csv')
df90 = pd.read_csv('f90Hz.csv')
df100 = pd.read_csv('f100Hz.csv')
df110 = pd.read_csv('f110Hz.csv')
df120 = pd.read_csv('f120Hz.csv')
df150 = pd.read_csv('f150Hz.csv')
df200 = pd.read_csv('f200Hz.csv')

filt_voltage_data_2 = df20['Voltage_V']
filt_voltage_data_4 = df40['Voltage_V']
filt_voltage_data_5 = df50['Voltage_V']
filt_voltage_data_6 = df60['Voltage_V']
filt_voltage_data_7 = df70['Voltage_V']
filt_voltage_data_8 = df80['Voltage_V']
filt_voltage_data_9 = df90['Voltage_V']
filt_voltage_data_10 = df100['Voltage_V']
filt_voltage_data_11 = df110['Voltage_V']
filt_voltage_data_12 = df120['Voltage_V']
filt_voltage_data_15 = df150['Voltage_V']
filt_voltage_data_20 = df200['Voltage_V']

v_pp_2 = filt_voltage_data_2.max() - filt_voltage_data_2.min()
v_pp_4 = filt_voltage_data_4.max() - filt_voltage_data_4.min()
v_pp_5 = filt_voltage_data_5.max() - filt_voltage_data_5.min()
v_pp_6 = filt_voltage_data_6.max() - filt_voltage_data_6.min()
v_pp_7 = filt_voltage_data_7.max() - filt_voltage_data_7.min()
v_pp_8 = filt_voltage_data_8.max() - filt_voltage_data_8.min()
v_pp_9 = filt_voltage_data_9.max() - filt_voltage_data_9.min()
v_pp_10 = filt_voltage_data_10.max() - filt_voltage_data_10.min()
v_pp_11 = filt_voltage_data_11.max() - filt_voltage_data_11.min()
v_pp_12 = filt_voltage_data_12.max() - filt_voltage_data_12.min()
v_pp_15 = filt_voltage_data_15.max() - filt_voltage_data_15.min()
v_pp_20 = filt_voltage_data_20.max() - filt_voltage_data_20.min()

freqs = np.array([20, 40, 50, 60 , 70, 80, 90, 100, 110, 120, 150, 200])
value = np.array([v_pp_2, v_pp_4, v_pp_5, v_pp_6, v_pp_7, v_pp_8, v_pp_9, v_pp_10, v_pp_11, v_pp_12, v_pp_15, v_pp_20])

db = 20*np.log10(value/5)

plt.plot(freqs, db, label = "Magnitude")
plt.title("Bode Plot for Low Pass Filter")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.axvline(x=72.34, color="red", linestyle="--", linewidth=1.5, label="Cutoff $f_c = 72.34Hz$")
plt.legend()
plt.savefig('bode_plot.pdf', format='pdf', bbox_inches='tight')
plt.show()