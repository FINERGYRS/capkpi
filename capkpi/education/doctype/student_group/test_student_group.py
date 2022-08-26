# Copyright (c) 2015, Finergy Reporting Solutions SAS (Finergy) and Contributors
# See license.txt

import unittest

import finergy

import capkpi.education


def get_random_group():
	doc = finergy.get_doc(
		{
			"doctype": "Student Group",
			"student_group_name": "_Test Student Group-" + finergy.generate_hash(length=5),
			"group_based_on": "Activity",
		}
	).insert()

	student_list = finergy.get_all("Student", limit=5)

	doc.extend("students", [{"student": d.name, "active": 1} for d in student_list])
	doc.save()

	return doc


class TestStudentGroup(unittest.TestCase):
	def test_student_roll_no(self):
		doc = get_random_group()
		self.assertEqual(max([d.group_roll_number for d in doc.students]), len(doc.students))

	def test_in_group(self):
		doc = get_random_group()

		last_student = doc.students[-1].student

		# remove last student
		doc.students = doc.students[:-1]
		doc.save()

		self.assertRaises(
			capkpi.education.StudentNotInGroupError,
			capkpi.education.validate_student_belongs_to_group,
			last_student,
			doc.name,
		)

		# safe, don't throw validation
		capkpi.education.validate_student_belongs_to_group(doc.students[0].student, doc.name)
