import sys
sys.path.append('/home/rewrie_code/test_repo')
import unittest
from func import calculate_pi_leibniz

class TestCalculatePiLeibniz(unittest.TestCase):
    def test_calculate_pi_leibniz(self):
        self.assertAlmostEqual(calculate_pi_leibniz(1), 4)
        self.assertAlmostEqual(calculate_pi_leibniz(2), 2.666666666666667)
        self.assertAlmostEqual(calculate_pi_leibniz(3), 3.466666666666667)
        self.assertAlmostEqual(calculate_pi_leibniz(4), 2.8952380952380956)
        self.assertAlmostEqual(calculate_pi_leibniz(5), 3.3396825396825403)

if __name__ == '__main__':
    unittest.main()