import sys


class Dependencies:
    def __init__(self, a=False):
        self.a = a


if __name__ == '__main__':
    dep = Dependencies(True)
    sys.exit(0)