# cython: profile=True, boundscheck=False, wraparound=False, nonecheck=False, cdivision = True
cimport cython
from libc.math cimport pow as c_pow
from libc.math cimport sqrt as c_sqrt

def cython_pot(double[:, :] r, double soft):
    cdef:
        int N = r.shape[0]
        double soft2 = c_pow(soft,2)
        double pot = 0.0
        int i, j
        double dr

    for i in range(N-1):
        for j in range(i+1,N):
            dr = 0.
            for k in range(3):
                dr += c_pow((r[i,k]-r[j,k]), 2)
            dr = c_sqrt(dr+soft2)
            pot += 1./dr
    return pot
