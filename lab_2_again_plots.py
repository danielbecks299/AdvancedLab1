import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

#read data
df0 = pd.read_csv("Trial #0.csv")
df1 = pd.read_csv("Trial #1.csv")

t0 = df0["Time_ms"].to_numpy()
R0 = df0["Resistance"].to_numpy()
T0 = df0["Temp_K"].to_numpy()

t1 = df1["Time_ms"].to_numpy()
R1 = df1["Resistance"].to_numpy()
T1 = df1["Temp_K"].to_numpy()

############################# PLOT RESISTANCE & TEMP ######################################################################

# Dedicated background baselines from R0 and T0
r_bg_mean = np.mean(R0)
t_bg_mean = np.mean(T0)

# Edge-to-edge centered rolling averages
window = 15
R1_smooth = (
    pd.Series(R1).rolling(window=window, center=True, min_periods=1).mean()
)
T1_smooth = (
    pd.Series(T1).rolling(window=window, center=True, min_periods=1).mean()
)

# Clean publication styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), dpi=300, sharex=True)

# --- Left Panel: Resistance R1(t) ---
ax1.plot(
    t1,
    R1,
    color="#7A99AC",
    alpha=0.45,
    linewidth=1.0,
    label="Raw $R_T$",
)
ax1.plot(
    t1,
    R1_smooth,
    color="#1B4965",
    linewidth=2.2,
    label=f"Smoothed ({window}-pt avg)",
)
ax1.axhline(
    r_bg_mean,
    color="#D95D39",
    linestyle="--",
    linewidth=1.3,
    label=f"Baseline ($\\overline{{R}}_0 = {r_bg_mean:.1f}\\,\\Omega$)",
)
ax1.fill_between(t1, r_bg_mean, R1_smooth, color="#1B4965", alpha=0.08)

ax1.set_title("(a) Thermistor Resistance vs. Time", pad=10, fontweight="bold")
ax1.set_xlabel("Time (s)", labelpad=8)
ax1.set_ylabel("Resistance ($\\Omega$)", labelpad=8)

# --- Right Panel: Temperature T1(t) in Kelvin ---
ax2.plot(
    t1,
    T1,
    color="#84A98C",
    alpha=0.45,
    linewidth=1.0,
    label="Raw $T$",
)
ax2.plot(
    t1,
    T1_smooth,
    color="#2D6A4F",
    linewidth=2.2,
    label=f"Smoothed ({window}-pt avg)",
)
ax2.axhline(
    t_bg_mean,
    color="#D95D39",
    linestyle="--",
    linewidth=1.3,
    label=f"Baseline ($\\overline{{T}}_0 = {t_bg_mean:.2f}$ K)",
)
ax2.fill_between(t1, t_bg_mean, T1_smooth, color="#2D6A4F", alpha=0.08)

ax2.set_title("(b) Thermistor Temperature vs. Time", pad=10, fontweight="bold")
ax2.set_xlabel("Time (s)", labelpad=8)
ax2.set_ylabel("Temperature (K)", labelpad=8)

# Shared grid, tick, and axis padding setup
for ax, data, bg in zip([ax1, ax2], [R1, T1], [r_bg_mean, t_bg_mean]):
    ax.grid(
        True, which="major", linestyle=":", linewidth=0.8, color="#CCCCCC", alpha=0.8
    )
    ax.minorticks_on()
    ax.tick_params(direction="in", which="both", top=False, right=False)

    d_min = min(np.nanmin(data), bg)
    d_max = max(np.nanmax(data), bg)
    margin = 0.08 * (d_max - d_min) if d_max > d_min else 0.05
    ax.set_ylim(d_min - margin, d_max + margin)
    ax.set_xlim(t1[0], t1[-1])
    ax.legend(frameon=True, facecolor="white", edgecolor="#E0E0E0", loc="best")

plt.tight_layout()
plt.savefig("thermistor_R_and_T_side_by_side.pdf", dpi=300, bbox_inches="tight")
plt.show()

############################# PLOT DELTA RESISTANCE & DELTA TEMP ######################################################################

# 1. Compute baseline-subtracted shifts using your dedicated background runs (R0, T0)
r_bg_mean = np.mean(R0)
t_bg_mean = np.mean(T0)

delta_R = np.asarray(R1) - r_bg_mean
delta_T = np.asarray(T1) - t_bg_mean

# Edge-to-edge rolling averages
window = 15
dR_smooth = (
    pd.Series(delta_R).rolling(window=window, center=True, min_periods=1).mean()
)
dT_smooth = (
    pd.Series(delta_T).rolling(window=window, center=True, min_periods=1).mean()
)

# 2. Configure clean, publication-grade styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), dpi=300, sharex=True)

# --- Left Panel: Delta R ---
ax1.plot(
    t1,
    delta_R,
    color="#7A99AC",
    alpha=0.45,
    linewidth=1.0,
    label="Raw $\\Delta R$",
)
ax1.plot(
    t1,
    dR_smooth,
    color="#1B4965",
    linewidth=2.2,
    label=f"Smoothed ({window}-pt avg)",
)
ax1.axhline(
    0,
    color="#D95D39",
    linestyle="--",
    linewidth=1.3,
    label=f"Baseline ($\\overline{{R}}_0 = {r_bg_mean:.1f}\\,\\Omega$)",
)
ax1.fill_between(t1, 0, dR_smooth, color="#1B4965", alpha=0.08)

ax1.set_title(
    "(a) Resistance Shift $\\Delta R(t)$", pad=10, fontweight="bold"
)
ax1.set_xlabel("Time (s)", labelpad=8)
ax1.set_ylabel("$\\Delta R = R(t) - \\overline{R}_0$ ($\\Omega$)", labelpad=8)

# --- Right Panel: Delta T ---
ax2.plot(
    t1,
    delta_T,
    color="#84A98C",
    alpha=0.45,
    linewidth=1.0,
    label="Raw $\\Delta T$",
)
ax2.plot(
    t1,
    dT_smooth,
    color="#2D6A4F",
    linewidth=2.2,
    label=f"Smoothed ({window}-pt avg)",
)
ax2.axhline(
    0,
    color="#D95D39",
    linestyle="--",
    linewidth=1.3,
    label=f"Baseline ($\\overline{{T}}_0 = {t_bg_mean:.2f}$ K)",
)
ax2.fill_between(t1, 0, dT_smooth, color="#2D6A4F", alpha=0.08)

ax2.set_title(
    "(b) Temperature Shift $\\Delta T(t)$", pad=10, fontweight="bold"
)
ax2.set_xlabel("Time (s)", labelpad=8)
ax2.set_ylabel("$\\Delta T = T(t) - \\overline{T}_0$ (K)", labelpad=8)

# 3. Consistent formatting, padding, and legends across both panels
for ax, data in zip([ax1, ax2], [delta_R, delta_T]):
    ax.grid(
        True, which="major", linestyle=":", linewidth=0.8, color="#CCCCCC", alpha=0.8
    )
    ax.minorticks_on()
    ax.tick_params(direction="in", which="both", top=False, right=False)

    d_min, d_max = np.nanmin(data), np.nanmax(data)
    margin = 0.08 * (d_max - d_min) if d_max > d_min else 0.05
    ax.set_ylim(d_min - margin, d_max + margin)
    ax.set_xlim(t1[0], t1[-1])
    ax.legend(frameon=True, facecolor="white", edgecolor="#E0E0E0", loc="best")

plt.tight_layout()
plt.savefig("thermistor_delta_R_delta_T.pdf", dpi=300, bbox_inches="tight")
plt.show()

############################# NEWTON COOLING ######################################################################

T_init_fixed = 296.58

def newtons_cooling_fixed_t0(t, T_env, tau):
  return T_env + (T_init_fixed - T_env) * np.exp(-(t - t[0]) / tau)


p0 = [t_bg_mean, 15.0]
popt, pcov = curve_fit(
    newtons_cooling_fixed_t0,
    t1,
    T1,
    p0=p0,
    bounds=([0.0, 1e-3], [1000.0, np.inf]),
    maxfev=10000,
)
T_env_fit, tau_fit = popt
tau_err = np.sqrt(np.diag(pcov))[1]

T_pred = newtons_cooling_fixed_t0(t1, *popt)
ss_res = np.sum((T1 - T_pred) ** 2)
ss_tot = np.sum((T1 - np.mean(T1)) ** 2)
r_squared = 1.0 - (ss_res / ss_tot)

print(f"Fixed T(t0)  : {T_init_fixed:.2f} K")
print(f"Fitted T_env : {T_env_fit:.2f} K (Baseline T0: {t_bg_mean:.2f} K)")
print(f"Time constant: tau = {tau_fit:.2f} ± {tau_err:.2f} s")
print(f"R^2          : {r_squared:.4f}")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

ax.plot(
    t1,
    T1,
    color="#84A98C",
    alpha=0.55,
    linewidth=1.1,
    label="Measured $T(t)$",
)
ax.plot(
    t1,
    T_pred,
    color="#C1292E",
    linewidth=2.2,
    label=(
        f"Newton Fit ($T_0 = {T_init_fixed:.1f}$ K, "
        f"$\\tau = {tau_fit:.2f}\\,\\mathrm{{s}}$, $R^2 = {r_squared:.3f}$)"
    ),
)
ax.axhline(
    t_bg_mean,
    color="#D95D39",
    linestyle="--",
    linewidth=1.3,
    label=f"Baseline ($\\overline{{T}}_0 = {t_bg_mean:.2f}$ K)",
)

ax.set_title(
    "Fit to Newton's Law of Cooling",
    pad=12,
    fontweight="bold",
)
ax.set_xlabel("Time (s)", labelpad=8)
ax.set_ylabel("Temperature (K)", labelpad=8)
ax.grid(
    True, which="major", linestyle=":", linewidth=0.8, color="#CCCCCC", alpha=0.8
)
ax.minorticks_on()
ax.tick_params(direction="in", which="both", top=False, right=False)
ax.set_xlim(t1[0], t1[-1])
ax.legend(frameon=True, facecolor="white", edgecolor="#E0E0E0", loc="best")

plt.tight_layout()
plt.savefig("thermistor_all_t1_newton_fit.pdf", dpi=300, bbox_inches="tight")
plt.show()