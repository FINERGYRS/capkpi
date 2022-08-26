# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

from capkpi.education.api import get_grade

# test_records = finergy.get_test_records('Assessment Result')


class TestAssessmentResult(unittest.TestCase):
	def test_grade(self):
		grade = get_grade("_Test Grading Scale", 80)
		self.assertEqual("A", grade)

		grade = get_grade("_Test Grading Scale", 70)
		self.assertEqual("B", grade)
