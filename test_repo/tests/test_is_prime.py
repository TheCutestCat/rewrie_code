import sys
sys.path.append('/home/rewrite2/gpt-engineer/test_repo/')
import unittest
from func import is_prime

class TestIsPrime(unittest.TestCase):
    
    def test_prime_number(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(19))
        self.assertTrue(is_prime(23))
        self.assertTrue(is_prime(29))
    
 
if __name__ == '__main__':
    unittest.main()