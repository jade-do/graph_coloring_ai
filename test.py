import unittest
import numpy as np
from main import start_coloring

class TestGraphColoring(unittest.TestCase):

    def test_input_1(self):
        fname = 'input1.txt'
        self.assertEqual(start_coloring(fname), "correct solution")

    def test_input_2(self):
        fname = 'input2.txt'
        self.assertEqual(start_coloring(fname), "correct solution")

    def test_input_3(self):
        fname = 'input3.txt'
        self.assertEqual(start_coloring(fname), "correct solution")

    def test_input_4(self):
        fname = 'input4.txt'
        self.assertEqual(start_coloring(fname), "correct solution")

    def test_input_5(self):
        fname = 'input5.txt'
        self.assertEqual(start_coloring(fname), "no solution")

    def test_input_6(self):
        fname = 'input6.txt'
        self.assertEqual(start_coloring(fname), "correct solution")

    def test_input_7(self):
        fname = 'input7.txt'
        self.assertEqual(start_coloring(fname), "correct solution")


if __name__ == "__main__":
    unittest.main()

