import unittest
import numpy as np

import displot.feature as feature
from displot.feature import *


class TestFeature(unittest.TestCase):
    def setUp(self):
        regionprops = type("regionprops", (), {
            "convex_image": np.array([
                [False, False, True, False],
                [False, True, True, True],
                [True, True, True, True],
                [False, True, True, False]
            ])
        })
        regionprops_larger = type("regionprops", (), {
            "convex_image": np.array([
                [False, False, True, True, True, False, False, False, False],
                [False, True, True, True, True, True, True, False, False],
                [True, True, True, True, True, True, True, True, False],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, False],
                [True, True, True, True, True, True, True, True, False],
                [False, True, True, True, True, True, True, True, False],
                [False, False, True, True, True, True, True, False, False],
                [False, False, False, True, False, False, False, False, False]
            ])
        })

        self.feature1 = feature.Feature((2,2), (0,0,4,4), regionprops)
        self.feature1_larger = feature.Feature((5,5), (0,0,9,9), regionprops_larger)
        self.feature2 = feature.Feature((4,2), (2,0,6,4), regionprops)
        self.feature3 = feature.Feature((5,2), (3,0,7,4), regionprops)
        self.feature4 = feature.Feature((22,22), (20,20,25,25), regionprops)
        self.feature5 = feature.Feature((2,2), (0,7,4,11), regionprops)

    def test_overlap_total(self):
        self.assertEqual(self.feature1_larger.overlap(self.feature1, True), (16,None,1,None))
        self.assertEqual(self.feature1.overlap(self.feature1_larger, True), (16,None,1,None))
        self.assertEqual(self.feature1_larger.overlap(self.feature1), (16,10,1,1))
        self.assertEqual(self.feature1.overlap(self.feature1_larger), (16,10,1,1))

    def test_overlap_half(self):
        self.assertEqual(self.feature2.overlap(self.feature1, True), (8,None,1/3,None))
        self.assertEqual(self.feature1.overlap(self.feature2, True), (8,None,1/3,None))
        self.assertEqual(self.feature2.overlap(self.feature1), (8,3,1/3,3/17))
        self.assertEqual(self.feature1.overlap(self.feature2), (8,3,1/3,3/17))

    def test_overlap_quarter(self):
        self.assertEqual(self.feature3.overlap(self.feature1, True), (4,None,1/7,None))
        self.assertEqual(self.feature1.overlap(self.feature3, True), (4,None,1/7,None))
        self.assertEqual(self.feature3.overlap(self.feature1), (4,1,1/7,1/19))
        self.assertEqual(self.feature1.overlap(self.feature3), (4,1,1/7,1/19))

    def test_overlap_different_size(self):
        self.assertEqual(self.feature5.overlap(self.feature1_larger, True), (8,None,8/89,None))
        self.assertEqual(self.feature1_larger.overlap(self.feature5, True), (8,None,8/89,None))
        self.assertEqual(self.feature5.overlap(self.feature1_larger), (8,2,8/89,0.031746031746031744))
        self.assertEqual(self.feature1_larger.overlap(self.feature5), (8,2,8/89,0.031746031746031744))

    def test_overlap_none(self):
        self.assertEqual(self.feature1.overlap(self.feature4), (0,0,0,0))
        self.assertEqual(self.feature4.overlap(self.feature1), (0,0,0,0))

if __name__ == '__main__':
    unittest.main()
