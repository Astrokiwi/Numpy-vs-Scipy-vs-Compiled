# Python_vs_Fortran

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

N= 1000
two_loop_pot         Result=941647.251511 Time=  2.701507
magic_index_pot      Result=941647.251511 Time=  0.046448
one_loop_pot         Result=941647.251511 Time=  0.023867
fortran_two_loop_pot Result=941647.251511 Time=  0.001878

numpy_sum            Result=1516.025408 Time=  0.000011
fortran_sum          Result=1516.025408 Time=  0.000007


N= 2000
two_loop_pot         Result=3748111.565650 Time= 10.963533
magic_index_pot      Result=3748111.565650 Time=  0.200737
one_loop_pot         Result=3748111.565650 Time=  0.073511
fortran_two_loop_pot Result=3748111.565650 Time=  0.006949

numpy_sum            Result=2975.426514 Time=  0.000013
fortran_sum          Result=2975.426514 Time=  0.000012


N= 5000
two_loop_pot         Result=23641083.151029 Time= 68.737083
magic_index_pot      Result=23641083.151033 Time=  1.299696
one_loop_pot         Result=23641083.151033 Time=  0.366119
fortran_two_loop_pot Result=23641083.151029 Time=  0.043064

numpy_sum            Result=7447.709515 Time=  0.000019
fortran_sum          Result=7447.709515 Time=  0.000037


Basically, the dumb Fortran loop is almost 10 times faster than the cleverer numpy loop. In this situation, it looks like I'm putting in more work to do the numpy loop,
but ending up with slower code. The Fortran code itself is extremely simple, and combining it with Python through f2py is a single line.

So here is the question: is this really the best solution here? Is a custom Fortran module really the best solution, even for this fairly simple problem, or is there a way
to do this more efficiently in numpy? And if there is a more efficient numpy solution, is it worth the effort to use a more complex algorithm when a trivial Fortran code is
faster? 
