print("importing and compiling")
import sys
import os
from time import time

try:
    import numpy as np
except:
    print("oh come on, you need numpy at the bare minimum")
    sys.exit()

try:
    import naive_pythran_pot
    pythran_loaded = True
except:
    pythran_loaded = False

try:
    from fort_pot import fort_pot
    fortran_loaded = True
except:
    fortran_loaded = False

try:
    #Cython code by Pip Grylls
    import pyximport; pyximport.install()
    from cython_pot import cython_pot
    cython_loaded = True
except:
    cython_loaded = False

try:
    import scipy.spatial.distance as ds
    scipy_loaded = True
except:
    scipy_loaded = False



# define numpy/scipy functions

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

#suggestion from Harry Rossides
def scipy_pot(r,soft):
   return (1./np.sqrt(ds.pdist(r, 'sqeuclidean')+soft*soft)).sum()

# Fortran wrappers
def fortran_two_loop_pot(r,soft):
    return fort_pot.two_loop_pot(r,soft)

def fortran_one_loop_pot(r,soft):
    return fort_pot.one_loop_pot(r,soft)

def fortran_sum(r,soft):
    return fort_pot.fortran_sum(r)

def numpy_sum(r,soft):
    return np.sum(r)

#function timer wrapper wrapper - could be a decorator?
def time_func(f):
    start = time()
    result = f(r,soft)
    end = time()
    print("%-20s Result=%10f Time=%10f"%(f.__name__,result,end-start))

if __name__ == "__main__":

    soft = 1.e-2

#     for N in [1000,2000,5000]:
    for N in [1000]:
        for repeat_runs in range(2):
            print("N=",N)

            r = np.random.random((N,3))
    
            time_func(two_loop_pot)
            time_func(magic_index_pot)
            time_func(one_loop_pot)
            time_func(scipy_pot)
            if cython_loaded:
                time_func(cython_pot)
            if pythran_loaded:
                time_func(naive_pythran_pot.naive_pythran_pot)
            if fortran_loaded:
                time_func(fortran_two_loop_pot)
                time_func(fortran_one_loop_pot)

            print("")

            time_func(numpy_sum)

            if fortran_loaded:
                time_func(fortran_sum)

            print("\n")

        os.system("julia potential_test.jl %d"%N) # can't get Julia to run with conda Python, run from terminal