import unittest
import io
from contextlib import redirect_stdout

from src.main import Dependencies


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.deps = Dependencies()

    def test_smoke(self):
        self.assertIsNotNone(self.deps)

    def test_sample(self):
        with open('../sample-out.txt') as inf:
            expected = inf.read().strip()
        with open('../sample.txt') as inf:
            commands = [x.strip().split() for x in inf.readlines()]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.deps.run_commands(commands)
        self.assertEqual(expected.strip(), buffer.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
