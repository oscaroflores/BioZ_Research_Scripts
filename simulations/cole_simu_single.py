import numpy as np

# circuit constants
C_M=1e-6 ## C_M capacitor
R_inf=22 ## extracelular resistance
R_0=430 ## intracelular

K_div=32

M_div=512
print("K", K_div)
print("M", M_div)

dac=128
# f=((32.768e3*M_div)/K_div)/dac
f=131e3
print("freq", f)

w = 2*np.pi*f
Z_RC = 1/(complex((1/R_0),(w*C_M)))
Z_Cole=R_inf+Z_RC
print(Z_Cole)