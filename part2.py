from ase.io import read
from ase.visualize import view  # <-- import view

mpstruct = read("Ti(SiO3)2.cif")

#view(mpstruct)

#create supercell

mp_super = mpstruct.repeat((1,1,2))

view(mp_super)