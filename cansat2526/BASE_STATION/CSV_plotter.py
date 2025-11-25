#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox


def open_csv():
    path = filedialog.askopenfilename(
        title="Válaszd ki a telemetria CSV-t",
        filetypes=[("CSV fájlok", "*.csv")]
    )

    if not path:
        return

    try:
        df = pd.read_csv(path)
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem tudom beolvasni a CSV-t:\n{e}")
        return

    plot_dataframe(df, path)


def plot_dataframe(df: pd.DataFrame, path: str):
    # Tengely kiválasztás: time_s → time → MET → index
    if "time" in df.columns:
        try:
            x = (
                df["time"]
                .astype(str)
                .str.replace("s", "", regex=False)
                .astype(float)
            )
            x_label = "Idő [s]"
        except:
            x = df.index
            x_label = "Minta index"
    elif "MET" in df.columns:
        x = df["MET"]
        x_label = "MET"
    else:
        x = df.index
        x_label = "Minta index"

    has_temp = "T_C" in df.columns
    has_rh = "RH_pct" in df.columns
    has_p = "P_hPa" in df.columns

    n = sum([has_temp, has_rh, has_p])
    if n == 0:
        messagebox.showerror("Hiba", "A fájlban nincs T_C / RH_pct / P_hPa oszlop.")
        return

    fig, axs = plt.subplots(n, 1, figsize=(12, 8), sharex=True, dpi=150)
    if n == 1:
        axs = [axs]

    idx = 0

    if has_temp:
        axs[idx].plot(x, df["T_C"], linestyle="-", linewidth=1.4, color="red", antialiased=True)
        axs[idx].set_ylabel("Hőmérséklet [°C]")
        axs[idx].grid(True, linestyle="--", alpha=0.4)
        idx += 1

    if has_rh:
        axs[idx].plot(x, df["RH_pct"], linestyle="-", linewidth=1.4, color="blue", antialiased=True)
        axs[idx].set_ylabel("Páratartalom [%]")
        axs[idx].grid(True, linestyle="--", alpha=0.4)
        idx += 1

    if has_p:
        axs[idx].plot(x, df["P_hPa"], linestyle="-", linewidth=1.4, color="green", antialiased=True)
        axs[idx].set_ylabel("Nyomás [hPa]")
        axs[idx].grid(True, linestyle="--", alpha=0.4)

    axs[-1].set_xlabel(x_label)
    fig.suptitle(f"Telemetria grafikon – {path}")
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


# GUI ablak
root = tk.Tk()
root.title("CanSat CSV Plotter")
root.geometry("380x140")

label = tk.Label(root, text="Válassz CSV fájlt a kirajzoláshoz", font=("Arial", 14))
label.pack(pady=15)

open_btn = tk.Button(root, text="📂 OPEN CSV", font=("Arial", 16), command=open_csv)
open_btn.pack(pady=10)

root.mainloop()