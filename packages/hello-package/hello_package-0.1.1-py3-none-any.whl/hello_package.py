import numpy as np


def calVecInPQW(a: float, e: float, E: float):
    """
    p = a*cosE -c
    q = b*sinE
    w = 0
    c=a*e
    b=a*sqrt(1-e**2)
    """
    b = a * np.sqrt(1 - e**2)
    c = a * e
    return np.array([a * np.cos(E) - c, b * np.sin(E), 0], dtype='float64')


def hello():
    print("Hello the world from package")


def parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("square", help="display a square of a given number", type=int)
    parser.add_argument("square2", help="display a square of a given number", type=int)
    args = parser.parse_args()
    print(args.square**args.square2)


if __name__ == "__main__":
    print(calVecInPQW(10, 0.1, 30))
