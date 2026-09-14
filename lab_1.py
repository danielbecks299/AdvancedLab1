import serial
import matplotlib.pyplot as plt
import numpy as np

arduino = serial.Serial("/dev/cu.usbmodem2101", 9600)

plt.plot()

v_in_array = []
v_out_array = []

def find_resist(R2, v_in_array, v_out_array):
    R1 = R2 / (v_in_array / v_out_array - 1)
    return R1

for i in range(5):
    line = arduino.readline().decode().strip()
    v_in, v_out = map(float, line.split())

    v_in_array.append(v_in)
    v_out_array.append(v_out)

arduino.close()

v_in_array = np.array(v_in_array)
v_out_array = np.array(v_out_array)

R2 = 1000
R1 = find_resist(R2, v_in_array, v_out_array)

final_R1 = np.mean(R1)
print(v_in_array)
print(v_out_array)
print(final_R1)

v_in_avg = np.mean(v_in_array)
R1_theoretical = np.linspace(0, 5000, 500) 
V_out_theoretical = v_in_avg * (R1_theoretical / (R2 + R1_theoretical))

plt.figure(figsize=(8, 5))
plt.plot(R1_theoretical, V_out_theoretical, 'b-', label=r'Calculated $R_1$', color='red')
plt.axvline(x=final_R1, color='black', linestyle='--', label=f'$R_1 = {final_R1}$')

plt.xlabel(r"$Theoretical \ R_1$")
plt.ylabel(r"$Theoretical \ V_{out}$")
plt.legend(title=r'Analytic Plot of $R_1 \ vs. \ V_{out}$')

plt.savefig("voltage_divider_plot.pdf")

plt.show()




