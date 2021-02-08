import unittest

from src.main import Dependencies


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.deps = Dependencies(True)

    def test_smoke(self):
        self.assertIsNotNone(self.deps)

    def test_init(self):
        self.assertTrue(self.deps.a)


if __name__ == '__main__':
    unittest.main()
