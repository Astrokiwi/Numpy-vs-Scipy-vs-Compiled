print("importing and compiling")
import sys
import os
from time import time

try:
    import numpy as np
except ImportError as e:
    print("oh come on, you need numpy at the bare minimum")
    raise e

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


def timed(f):
    """
        timed(f)
    
    A wrapper to pass the global arrays (position and softening) to a function,
    and print the result, the name of the function, and the execution time
    """
    def tf():
        start = time()
        result = f(r,soft)
        end = time()
        print("%-20s Result=%10f Time=%10f"%(f.__name__,result,end-start))
    return tf

# define numpy/scipy functions

@timed
def two_loop_pot(r,soft):
    """
        two_loop_pot(r,soft)

    Simple N^2 loop, doing 3-vector sums to calculate potential
    """
    N = r.shape[0]    
    pot = 0.
    soft2 = soft**2
    for i in range(N-1):
        for j in range(i+1,N):
            dr = np.sqrt(np.sum((r[i,:]-r[j,:])**2)+soft2)
            pot += 1./dr
    return pot

@timed
def one_loop_pot(r,soft):
    """
        one_loop_pot(r,soft)

    Collect the potential sum into a single loop so that more work is
    done in compiled numpy. This may create big intermediate arrays,
    but turns out reasonably fast
    """
    N = r.shape[0]    
    pot = 0.
    soft2 = soft**2
    for i in range(N-1):
        dr = np.sqrt(np.sum((r[i,:]-r[i+1:,:])**2,axis=1)+soft2)
        pot += np.sum(1./dr)
    return pot

@timed
def magic_index_pot(r,soft):
    """
        magic_index_pot(r,soft)

    Use more complex indexing to calculate the potential without any
    explicit Python loop. This actually turns out somewhat slow
    """
    N = r.shape[0]
    soft2 = soft**2
    indices = np.broadcast_to(range(N),(N,N)).T
    dr = np.sqrt(np.sum((r[:,:] - r[indices,:])**2,axis=2)+soft2)
    pot = np.sum(np.tril(1./dr,-1))
    return pot

#suggestion from Harry Rossides
@timed
def scipy_pot(r,soft):
    """
        scipy_pot(r,soft)

    Use an existing library to do most of the hard work. Great if the
    library function exists, but the point of this is to show how different
    methods work *in principle* and you can't always assume a library
    has already implemented what you want!
    """
    return (1./np.sqrt(ds.pdist(r, 'sqeuclidean')+soft*soft)).sum()

# Fortran wrappers
@timed
def fortran_two_loop_pot(r,soft):
    """
        fortran_two_loop_pot(r,soft)

    Wrapper for an f2py function to make it pickleable. Same method as
    two_loop_pot, but precompiled.
    """
    return fort_pot.two_loop_pot(r,soft)

@timed
def fortran_one_loop_pot(r,soft):
    """
        fortran_one_loop_pot(r,soft)

    Wrapper for an f2py function to make it pickleable. Same method as
    one_loop_pot, but precompiled.
    """
    return fort_pot.one_loop_pot(r,soft)

@timed
def fortran_sum(r,soft):
    """
        fortran_sum(r,soft)

    Wrapper for an f2py function to make it pickleable. Simple O(N)
    sum to compare with numpy
    """
    return fort_pot.fortran_sum(r)

@timed
def numpy_sum(r,soft):
    """
        numpy_sum(r,soft)

    Simple O(N) sum to show numpy's performance when entirely relying
    on a library function
    """
    return np.sum(r)

if __name__ == "__main__":

    soft = 1.e-2

#     for N in [1000,2000,5000]:
    for N in [1000]:
        for repeat_runs in range(2):
            print("N=",N)
            if repeat_runs==0:
                print("First run - just in case anything needs to be 'just-in-time' compiled")
            else:
                print("Second run - everything should be compiled")

            r = np.random.random((N,3))
    
            two_loop_pot()
            magic_index_pot()
            one_loop_pot()
            scipy_pot()
            if cython_loaded:
                timed_cython = timed(cython_pot)
                timed_cython()
            if pythran_loaded:
                timed_pythran = timed(naive_pythran_pot.naive_pythran_pot)
                timed_pythran()
            if fortran_loaded:
                fortran_two_loop_pot()
                fortran_one_loop_pot()

            print("")

            numpy_sum()

            if fortran_loaded:
                fortran_sum()

            print("\n")

        os.system("julia potential_test.jl %d"%N) # can't get Julia to run with conda Python, run from terminal