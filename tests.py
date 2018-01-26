import numpy as np
from fort_pot import fort_pot
from time import time

def two_loop_pot(r,soft):
    N = r.shape[0]    
    pot = 0.
    soft2 = soft**2
    for i in range(N-1):
        for j in range(i+1,N):
            dr = np.sqrt(np.sum((r[i,:]-r[j,:])**2)+soft2)
            pot += 1./dr
    return pot

def one_loop_pot(r,soft):
    N = r.shape[0]    
    pot = 0.
    soft2 = soft**2
    for i in range(N-1):
        dr = np.sqrt(np.sum((r[i,:]-r[i+1:,:])**2,axis=1)+soft2)
        pot += np.sum(1./dr)
    return pot

def magic_index_pot(r,soft):
    N = r.shape[0]
    soft2 = soft**2
    indices = np.broadcast_to(range(N),(N,N)).T
    dr = np.sqrt(np.sum((r[:,:] - r[indices,:])**2,axis=2)+soft2)
    pot = np.sum(np.tril(1./dr,-1))
    return pot

def fortran_two_loop_pot(r,soft):
    return fort_pot.two_loop_pot(r,soft)

def fortran_sum(r,soft):
    return fort_pot.fortran_sum(r)

def numpy_sum(r,soft):
    return np.sum(r)

soft = 1.e-2

def time_func(f):
    start = time()
    result = f(r,soft)
    end = time()
    print("%-20s Result=%10f Time=%10f"%(f.__name__,result,end-start))


for N in [1000,2000,5000]:
    print("N=",N)

    r = np.random.random((N,3))
    
    time_func(two_loop_pot)
    time_func(magic_index_pot)
    time_func(one_loop_pot)
    time_func(fortran_two_loop_pot)

    print("")

    time_func(numpy_sum)
    time_func(fortran_sum)

    print("\n")

