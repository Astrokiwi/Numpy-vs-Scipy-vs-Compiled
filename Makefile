everything:
	f2py --opt=-O3 -c fort_pot.f90 -m fort_pot
# 	f2py2.7 --opt=-O3 -c fort_pot.f90 -m fort_pot
	pythran naive_pythran_pot.py

clean:
	rm *.o *.mod