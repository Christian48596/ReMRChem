from vampyr import vampyr3d as vp
from orbital4c import orbital as orb
from orbital4c import complex_fcn as cf
import numpy as np
import pytest
from scipy.special import legendre, laguerre, erf, gamma
from scipy.special import gamma
from scipy.constants import hbar

c = 137   # NOT A GOOD WAY. MUST BE FIXED!!!

mra = vp.MultiResolutionAnalysis(box=[-60,60], order=4)
prec = 1.0e-3
orb.orbital4c.light_speed = c
orb.orbital4c.mra = mra
cf.complex_fcn.mra = mra

def test_spinor():
    print("test_spinor")
    origin = [0.1, 0.2, 0.3]  # origin moved to avoid placing the nuclar charge on a node
    a_coeff = 3.0
    b_coeff = np.sqrt(a_coeff/np.pi)**3
    gauss = vp.GaussFunc(b_coeff, a_coeff, origin)
    gauss_tree = vp.FunctionTree(mra)
    vp.advanced.build_grid(out=gauss_tree, inp=gauss)
    vp.advanced.project(prec=prec, out=gauss_tree, inp=gauss)
    gauss_tree.normalize()
    spinor_H = orb.orbital4c()
    La_comp = cf.complex_fcn()
    La_comp.copy_fcns(real = gauss_tree)
    spinor_H.copy_components(La = La_comp)
    spinor_H.init_small_components(prec/10)
    spinor_H.normalize()
    val = spinor_H.comp_array[0].real([0.0, 0.0, 0.0])
    print(val)
    assert val == pytest.approx(0.5937902746013326)

def test_read():
    print("test_read")
    spinorb1 = orb.orbital4c()
    spinorb2 = orb.orbital4c()
    spinorb1.read("trees/spinorb1")
    spinorb2.read("trees/spinorb2")
    val1 = spinorb1.comp_array[0].real([0.0, 0.0, 0.0])
    val2 = spinorb2.comp_array[3].imag([0.0, 0.0, 0.0])
    print(val1, val2)
    assert val1 == pytest.approx(1.3767534073967547)
    assert val2 == pytest.approx(-0.012619848367561309)

#def test_mul():
#    print("test_mul")
#    spinorb1 = orb.orbital4c()

    
