import sys, unittest
from ase import units
from ase.lattice.cubic import FaceCenteredCubic
from ase.calculators.emt import EMT
from md import calcenergy

class MdTests(unittest.TestCase):

    def test_calcenergy(self):
        #Create test-crystal
        atoms = FaceCenteredCubic(
            directions = [[1,0,0],[0,1,0],[0,0,1]],
            symbol = "Cu",
            size=(2,2,2),
            pbc = True
        )

        #Attach calc
        atoms.calc = EMT()

        #Call our function, with this atom
        epot, ekin, etot, temp = calcenergy(atoms)

        #Check if values are float
        self.assertIsInstance(epot, float)
        self.assertIsInstance(ekin, float)
        self.assertIsInstance(etot, float)
        self.assertIsInstance(temp, float)

        #Check if resonable results
        self.assertAlmostEqual(etot, ekin + epot, places=10) #Same up to 10 decimals
        self.assertGreaterEqual(temp,0)


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())