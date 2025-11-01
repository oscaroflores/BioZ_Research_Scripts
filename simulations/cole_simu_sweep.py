import numpy as np

# circuit constants
C_M=15.25e-6 ## C_M capacitor
R_inf=22.953 ## extracelular resistance
R_0=429.14 ## intracelular

## iterate through frequencies
inc=1

for i in range(6):
    K_div=32/(pow(2,i))
    for i in range(33):
        M_div=512+(i*8)
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