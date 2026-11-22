import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

arduino = serial.Serial("/dev/cu.usbmodem1101", 115200)

#find temperature
def resistance_to_temp(R_t, r25=3300.0):
    A1 = 3.354016e-03
    B1 = 2.569850e-04
    C1 = 2.620131e-06
    D1 = 6.383091e-08

    # resistance to temp
    ln_r = np.log(R_t / r25)
    inv_t = A1 + B1 * ln_r + C1 * (ln_r**2) + D1 * (ln_r**3)
    return (1.0 / inv_t)

for i in range(2):
  input(f"Start Trial {i}: ")

  time_array = []
  A0_array = []

  # Collection loop
  while len(time_array) <= 600:
    line = arduino.readline().decode().strip()
    if line:
      try:
        t, A0 = map(float, line.split(","))
        time_array.append(t/1000)
        A0_array.append(A0)
      except ValueError:
        continue

  # convert to volts
  raw_signal = np.array(A0_array, dtype=float)
  v_out = raw_signal / 204.6

  # Find the resistance of the thermistor
  R1 = 1000
  R_t = R1 * ((5/v_out)-1)

  # convert to temp
  temp = resistance_to_temp(R_t)

  # Save file 
  df_run = pd.DataFrame({"Time_ms": time_array, "Resistance": R_t, "Temp_K": temp})
  filename = f"Trial #{i}.csv"
  df_run.to_csv(filename, index=False)
  print(f"Saved: {filename}")

arduino.close()
