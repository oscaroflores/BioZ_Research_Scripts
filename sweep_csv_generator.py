"""
Generate a MAX30009 BioZ calibration sweep CSV.

This script sweeps KDIV in {32, 16, 8, 4, 2, 1} and MDIV in [512..768] (step 8),
prints example Cole-model values, and writes rows to a CSV with columns:
CLK_FREQ_SEL, MDIV_MSB, MDIV_LSB, NDIV, KDIV, BIOZ_DAC_OSR, BIOZ_ADC_OSR,
I_COEF, Q_COEF, I_PHASE_COEF, Q_PHASE_COEF, I_OFFSET, Q_OFFSET.

Usage
  $ python3 cole_csv.py

Output
  SWEEP_MAX30009_calibration_values_YYYY-MM-DD_HH-MM-SS.csv (next to this script)

Requirements
  Python 3.9+, numpy

Notes
  - Docstrings follow PEP 257 and reStructuredText so pydoc/Sphinx can render them.
  - Prefer argparse for CLI options and --help if you add parameters later.
"""
import numpy as np
import csv
from datetime import datetime
from pathlib import Path

f_array = [
    4096, # K divider = 32
    8192, # = 16
    16.384e3, # 8
    32.768e3, # 4
    65.536e3, # 2
    131.072e3, # 1
]

# circuit constants
C_M=15.25e-6 ## C_M capacitor
R_inf=22.953 ## extracelular resistance
R_0=429.14 ## intracelular

## iterate through frequencies
inc=1

# Prepare CSV output
headers = [
    "CLK_FREQ_SEL", "MDIV_MSB", "MDIV_LSB", "NDIV", "KDIV",
    "BIOZ_DAC_OSR", "BIOZ_ADC_OSR",
    "I_COEF", "Q_COEF", "I_PHASE_COEF", "Q_PHASE_COEF", "I_OFFSET", "Q_OFFSET"
]
out_path = Path(__file__).with_name(f"SWEEP_MAX30009_calibration_values_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")

with out_path.open("w", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(headers)

    for i in range(6):
        K_div=32/(pow(2,i))          # 32,16,8,4,2,1
        KDIV_reg = 5 - i             # matches your sample CSV: 5..0

        for j in range(33):          # MDIV: 512..768 step 8
            M_div=512+(j*8)
            # CSV fields
            mdiv_msb = (M_div >> 8) & 0xFF
            mdiv_lsb = M_div & 0xFF

            # keep your existing calculations/prints
            print(inc,")")
            print("K", K_div)
            print("M", M_div)

            dac=128
            f=((32.768e3*M_div)/K_div)/dac
            print("freq", f)

            w = 2*np.pi*f
            Z_RC = 1/(complex((1/R_0),(w*C_M)))
            Z_Cole=R_inf+Z_RC
            print(Z_Cole)
            inc=inc+1
            print("\n")

            # write one CSV row per sweep point
            writer.writerow([
                1,            # CLK_FREQ_SEL
                mdiv_msb,     # MDIV_MSB
                mdiv_lsb,     # MDIV_LSB
                0,            # NDIV
                KDIV_reg,     # KDIV (5..0)
                2,            # BIOZ_DAC_OSR
                7,            # BIOZ_ADC_OSR
                1,            # I_COEF
                1,            # Q_COEF
                0,            # I_PHASE_COEF
                0,            # Q_PHASE_COEF
                0,            # I_OFFSET
                0,            # Q_OFFSET
            ])

print(f"Wrote CSV: {out_path}")