import unittest

def fun(x):
    return x + 1

class TestA(unittest.TestCase):
    def test1(self):
        self.assertEqual(fun(3), 4)

class TestB(unittest.TestCase):
    def test2(self):
        assert(fun(3) == 4)

if __name__ == '__main__':
    tests = [TestA, TestB]
    loader = unittest.TestLoader()
    test_suit = []

    for test in tests:
        suite = loader.loadTestsFromTestCase(test)
        test_suit.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)		
