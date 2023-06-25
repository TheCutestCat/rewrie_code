import sys
sys.path.append('/home/rewrie_code/test_repo')
import unittest
from func import calculate_sum

class TestCalculateSum(unittest.TestCase):
    def test_calculate_sum(self):
        numbers = [1, 2, 3, 4, 5]
        result = calculate_sum(numbers)
        self.assertEqual(result, 15)

        numbers = [10, 20, 30, 40, 50]
        result = calculate_sum(numbers)
        self.assertEqual(result, 150)

        numbers = [0, 0, 0, 0, 0]
        result = calculate_sum(numbers)
        self.assertEqual(result, 0)

        numbers = [-1, -2, -3, -4, -5]
        result = calculate_sum(numbers)
        self.assertEqual(result, -15)

if __name__ == '__main__':
    unittest.main()