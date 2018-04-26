# Python_vs_Fortran

## To use

You need `gfortran` and f2py2.7 installed, as well as Python2.7, with numpy and scipy. We use Python2.7 because it's required by Pythran Clone the repo, and go to its directory in your terminal. Then:

```
make
python tests.py
```

C'est tout.

## What/why?

This is an example of a fairly simple calculation that I can't figure out how to do efficiently in Python using the numpy library.
I find with complex algorithms, it often makes sense to code them in C or Fortran, but from time to time I find examples of fairly
simple problems that don't appear to have an easy efficient solution in numpy, but have a trivial solution in Fortran.
This particularly comes up in O(N^2) type problems, where for some vector of values a_i, I want to calculate a matrix of values
i.e. A_{i,j} = f(a_i,a_j), or something like a vector b_i = sum_j{f(a_i,a_j)}

As an example, here I calculate the potential of a bunch of points, distributed randomly in three dimensions, using a "softened" potential.
This is a fairly simple calculation, but it doesn't appear to be simple to calculate it quickly in Python.

I use a "two loop" naive method in both Python and Fortran, a "one loop" cleverer method in Python, and a "magic index" cleverest method in Python.
By comparison, I also do a direct O(N) sum of all the position coordinates, to show that numpy can actually be just as fast as Fortran if you're
able to let numpy do all the work as intended.

The results I get myself are:

```
('N=', 1000)
two_loop_pot         Result=937094.502420 Time=  2.691333
magic_index_pot      Result=937094.502420 Time=  0.045650
one_loop_pot         Result=937094.502420 Time=  0.023352
scipy_pot            Result=937094.502420 Time=  0.003214
naive_pythran_pot    Result=937094.502420 Time=  0.001762
fortran_two_loop_pot Result=937094.502420 Time=  0.001755

numpy_sum            Result=1493.812211 Time=  0.000012
fortran_sum          Result=1493.812211 Time=  0.000006


('N=', 2000)
two_loop_pot         Result=3786563.248134 Time= 10.923428
magic_index_pot      Result=3786563.248134 Time=  0.201008
one_loop_pot         Result=3786563.248134 Time=  0.071522
scipy_pot            Result=3786563.248134 Time=  0.018071
naive_pythran_pot    Result=3786563.248134 Time=  0.006900
fortran_two_loop_pot Result=3786563.248134 Time=  0.006863

numpy_sum            Result=3013.170319 Time=  0.000015
fortran_sum          Result=3013.170319 Time=  0.000009


('N=', 5000)
two_loop_pot         Result=23465072.621252 Time= 68.933690
magic_index_pot      Result=23465072.621249 Time=  1.284691
one_loop_pot         Result=23465072.621249 Time=  0.360706
scipy_pot            Result=23465072.621249 Time=  0.143408
naive_pythran_pot    Result=23465072.621252 Time=  0.042692
fortran_two_loop_pot Result=23465072.621252 Time=  0.042433

numpy_sum            Result=7538.788984 Time=  0.000036
fortran_sum          Result=7538.788984 Time=  0.000034
```

Basically, the dumb Fortran loop is almost 10 times faster than the cleverer numpy loop. In this situation, it looks like I'm putting in more work to do the numpy loop,
but ending up with slower code. The Fortran code itself is extremely simple, and combining it with Python through f2py is a single line.

So here is the question: is this really the best solution here? Is a custom Fortran module really the best solution, even for this fairly simple problem, or is there a way
to do this more efficiently in numpy? And if there is a more efficient numpy solution, is it worth the effort to use a more complex algorithm when a trivial Fortran code is
faster? 
