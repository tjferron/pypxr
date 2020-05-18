import refnx.util.general as general
import refnx
import numpy as np
import os
from numpy.testing import assert_almost_equal, assert_, assert_allclose


def test_version():
    # check that we can retrieve a version string
    refnx.__version__


class TestGeneral(object):
    def setup_method(self):
        self.pth = os.path.dirname(os.path.abspath(__file__))

    def test_q(self):
        q = general.q(1., 2.)
        assert_almost_equal(q, 0.1096567037)

    def test_q2(self):
        qx, qy, qz = general.q2(1., 2., 0., 2.)
        assert_almost_equal(qz, 0.1096567037)

    def test_wavelength_velocity(self):
        speed = general.wavelength_velocity(20.)
        assert_almost_equal(speed, 197.8017006541796, 5)

    def test_wavelength(self):
        wavelength = general.wavelength(0.1096567037, 1.)
        assert_almost_equal(wavelength, 2.)

    def test_angle(self):
        angle = general.angle(0.1096567037, 2.)
        assert_almost_equal(angle, 1.)

    def test_dict_compare(self):
        c = {'f': np.arange(10)}
        d = {'f': np.arange(10)}

        assert_(general._dict_compare(c, d))

        d = {'f': np.arange(11)}
        assert_(not general._dict_compare(c, d))

        d = {'f': 2}
        assert_(not general._dict_compare(c, d))

        assert_(general._dict_compare({'a': 1}, {'a': 1}))

    def test_neutron_transmission(self):
        try:
            import periodictable as pt
        except ImportError:
            return

        mat = pt.formula('N2', density=1.25e-3)
        ntd = general._neutron_transmission_depth(mat, 2)
        assert_allclose(ntd, 1365.8010284973458 * 10)

        t = general.neutron_transmission('N2', 1.25e-3, 2,
                                         1365.8010284973458 * 10)
        assert_almost_equal(t, np.exp(-1.))

        # check that we can vectorise
        t = general.neutron_transmission('N2', 1.25e-3, [2, 2.],
                                         [1365.8010284973458 * 10] * 2)
        assert_almost_equal(t, [np.exp(-1.)] * 2)
