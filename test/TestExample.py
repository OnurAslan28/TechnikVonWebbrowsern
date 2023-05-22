import unittest

from util.CollectionUtil import count


class TestClass(unittest.TestCase):
    def test_strings_a(self):
        count(5)
        self.assertEqual('a' * 4, 'aaaa')


if __name__ == "__main__":
    test = TestClass()
    test.test_strings_a()
    print("Everything passed")
