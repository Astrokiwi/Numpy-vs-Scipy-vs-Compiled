fort_pot:
	f2py --opt=-O3 -c fort_pot.f90 -m fort_pot

clean:
	rm *.o *.mod