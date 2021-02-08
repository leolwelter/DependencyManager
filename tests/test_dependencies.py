import unittest

from src.main import Dependencies


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.deps = Dependencies()

    def test_smoke(self):
        self.assertIsNotNone(self.deps)

if __name__ == '__main__':
    unittest.main()
