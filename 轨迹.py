___author___ = '陈鑫宇'
___version___ = '1.0.0'


from pymatgen.io.vasp.outputs import Vasprun, Poscar
import copy
import re

sd = []
l = 0
with open("POSCAR", "r") as f:
    for line in f:
        if l >= 9:
            d = []
            try:
                x, y, z, xsd, ysd, zsd = re.split("\s+", line.strip())
            except:
                break
            for g in [xsd.strip(), ysd.strip(), zsd.strip()]:
                if g == "T":
                    d.append(True)
                elif g == "F":
                    d.append(False)
            sd.append(d)
        l += 1

vasprun = Vasprun('vasprun.xml')
initial_structure = vasprun.initial_structure
new_structure = copy.deepcopy(initial_structure)
start_step = 0
end_step = 1000
gap = 5
for step in range(start_step, end_step, gap):
    ss = vasprun.ionic_steps[step]['structure']
    for i in range(len(ss)):
        site = ss[i]
        if site.species_string == "Li":
            new_structure.append(site.specie, site.frac_coords, properties={'selective_dynamics': sd[i]})
poscar = Poscar(new_structure)
poscar.write_file("li.vasp")
