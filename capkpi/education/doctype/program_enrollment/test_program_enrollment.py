# Copyright (c) 2015, Finergy and Contributors
# See license.txt

import unittest

import finergy

from capkpi.education.doctype.program.test_program import make_program_and_linked_courses
from capkpi.education.doctype.student.test_student import create_student, get_student


class TestProgramEnrollment(unittest.TestCase):
	def setUp(self):
		create_student(
			{
				"first_name": "_Test Name",
				"last_name": "_Test Last Name",
				"email": "_test_student@example.com",
			}
		)
		make_program_and_linked_courses("_Test Program 1", ["_Test Course 1", "_Test Course 2"])

	def test_create_course_enrollments(self):
		student = get_student("_test_student@example.com")
		enrollment = student.enroll_in_program("_Test Program 1")
		course_enrollments = student.get_all_course_enrollments()
		self.assertTrue("_Test Course 1" in course_enrollments.keys())
		self.assertTrue("_Test Course 2" in course_enrollments.keys())
		finergy.db.rollback()

	def tearDown(self):
		for entry in finergy.db.get_all("Course Enrollment"):
			finergy.delete_doc("Course Enrollment", entry.name)

		for entry in finergy.db.get_all("Program Enrollment"):
			doc = finergy.get_doc("Program Enrollment", entry.name)
			doc.cancel()
			doc.delete()
