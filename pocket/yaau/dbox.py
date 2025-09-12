from pymol import cmd
import numpy as np
def center_of(sel):
    m = cmd.get_model(sel)
    c = np.array([a.coord for a in m.atom]).mean(axis=0)
    print(sel, "center:", tuple(c))
center_of("pocket7")
