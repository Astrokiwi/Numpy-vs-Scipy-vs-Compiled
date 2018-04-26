import numpy as np

#pythran export naive_pythran_pot(float[][], float)
def naive_pythran_pot(r,soft):
    N = r.shape[0]    
    pot = 0.
    soft2 = soft**2
    for i in range(N-1):
        for j in range(i+1,N):
            dr = 0.
            for k in range(3):
                dr +=(r[i,k]-r[j,k])**2
            dr = np.sqrt(dr+soft2)
            pot += 1./dr
    return pot
