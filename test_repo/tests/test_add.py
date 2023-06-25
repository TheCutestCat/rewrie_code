import sys
sys.path.append('/home/rewrite2/gpt-engineer/test_repo/')
import unittest
from func import add

class TestAdd(unittest.TestCase):
    def test_add(self):
        result = add(2, 3)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()