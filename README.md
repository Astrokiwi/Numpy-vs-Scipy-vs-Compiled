# Simple potential sum benchmark for comparing Numpy, Scipy, f2py, and Julia

## To use

You need `gfortran`, `f2py`, `Julia`, and `Cython` installed, as well as `Python` with `numpy` and `scipy`. There is an option to try `pythran` too, but I've not really supported it - it required Python2.7 when I first started this repo.

Clone the repo, and go to its directory in your terminal. Then:

```
make
python tests.py
```

C'est tout.

## What/why?

This is an example of a fairly simple calculation that I can't figure out how to do efficiently in Python using the numpy library.
I find with complex algorithms, it often makes sense to code them in a compiled language, but from time to time I find examples of fairly
simple problems that don't appear to have an easy efficient solution in numpy, but have a trivial solution in something like Fortran.
This particularly comes up in O(N^2) type problems, where for some vector of values a_i, I want to calculate a matrix of values
i.e. A_{i,j} = f(a_i,a_j), or something like a vector b_i = sum_j{f(a_i,a_j)}

As an example, here I calculate the potential of a bunch of points, distributed randomly in three dimensions, using a "softened" potential.
This is a fairly simple calculation, but it doesn't appear to be simple to calculate it quickly in Python.

I use a "two loop" naive method in Python, Fortran, Cython, and Pythran, a "one loop" cleverer method in both Python and Fortran, a "magic index" clevererer method in Python, and a `scipy` cleverest method in Python. In Julia, I implement the one loop and two loop forms, but also a further unravelled "three loop" form, where the sum of the 3-vectors is also explicitly unravelled. The Cython version also uses the tree loop form.

By comparison, I also do a direct O(N) sum of all the position coordinates, to show that numpy can actually be about as fast as Fortran if you're
able to let numpy do all the work as intended.

Everything is run twice, just to clear out any "just in time" compilations that might dominate the computation time. I think we've got it set up now so that all the compilations are done ahead of time though.

The results I get myself are:

```
```importing and compiling
N= 1000
First run - just in case anything needs to be 'just-in-time' compiled
two_loop_pot         Result=919503.068947 Time=  3.917400
magic_index_pot      Result=919503.068947 Time=  0.150114
one_loop_pot         Result=919503.068947 Time=  0.048202
scipy_pot            Result=919503.068947 Time=  0.009160
cython_pot           Result=919503.068947 Time=  0.004740
naive_pythran_pot    Result=919503.068947 Time=  2.873673
fortran_two_loop_pot Result=919503.068947 Time=  0.004374
fortran_one_loop_pot Result=920874.508384 Time=  0.005165

numpy_sum            Result=1510.635577 Time=  0.000031
fortran_sum          Result=1510.635577 Time=  0.000008


N= 1000
Second run - everything should be compiled
two_loop_pot         Result=938903.692583 Time=  4.288951
magic_index_pot      Result=938903.692583 Time=  0.062831
one_loop_pot         Result=938903.692583 Time=  0.053735
scipy_pot            Result=938903.692583 Time=  0.004250
cython_pot           Result=938903.692583 Time=  0.004406
naive_pythran_pot    Result=938903.692583 Time=  2.884020
fortran_two_loop_pot Result=938903.692583 Time=  0.004511
fortran_one_loop_pot Result=940878.335147 Time=  0.005559

numpy_sum            Result=1495.110643 Time=  0.000042
fortran_sum          Result=1495.110643 Time=  0.000010


N=1000
First Julia run to compile everything
julia threeloop  0.004722 seconds
julia twoloop  0.311685 seconds (2.00 M allocations: 114.326 MiB, 20.26% gc time)
julia oneloop  0.019122 seconds (13.30 k allocations: 19.821 MiB, 7.87% gc time)
Julia run, with everything compiled (hopefully)
julia threeloop  0.004425 seconds
julia twoloop  0.259677 seconds (2.00 M allocations: 114.326 MiB, 3.61% gc time)
julia oneloop  0.015529 seconds (13.30 k allocations: 19.821 MiB, 8.97% gc time)
```

## Conclusions

- A big dumb series of nested loops is terrible in pure Python, but works really well in any compiled form. You can use numpy array operations to speed things up quite a lot though, up to maybe 8-9 times slower than the compiled form.

- All of the compiled forms take about the same time, so it doesn't matter if you use Cython, Julia, or Fortran (it's probably best to stick to whichever one you already know). Earlier tests also found Pythran was similar. Of course, the specific order of these three depends on your hardware, compiler, optimisation options etc, but I find they're all generally comparable.

- Julia seems to still be finicky about how you write your loops, and you can actually write more concise code in Fortran without losing efficiency.

- If you really dig through the libraries, you might find a scipy function that *almost* does what you want anyway, at about 1/3rd the speed of writing out the loop explicitly and compiling it. This gives more compact code, but it took multiple people searching the docs to find the one correct function.

## Appendices:

### Clarification
Before somebody "corrects" me: of course the numpy and scipy libraries are compiled as well. I'm really making the comparison between using standard libraries, and writing your own custom loops. The point is that there are fairly simple nested loops that the standard numerical libraries don't cover easily, and even if you do eventually find a library function that is kinda what you want, you might do better to use something compiled like Cython or f2py.

### Why bother with Fortran?
Because Fortran has nice array syntax, and writing heavy numerical work in Fortran is really not all that different form writing it in Python. Many people in the numerical field have experience with Fortran, and then using f2py can come out simpler than trying to figure out Cython. The code ends up almost looking identical anyway - Fortran just has more verbose variable declarations, and index-1 arrays. There is very little difference between Cython code and Fortran. Of course, if you already know Python, there's no point to learn a new language to do something you can already do in Cython. Fortran compilers are also more mature than Julia compilers, and seem to provide better optimisations.
