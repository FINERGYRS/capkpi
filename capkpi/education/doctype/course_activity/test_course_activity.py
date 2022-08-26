# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestCourseActivity(unittest.TestCase):
	pass


def make_course_activity(enrollment, content_type, content):
	activity = finergy.get_all(
		"Course Activity",
		filters={"enrollment": enrollment, "content_type": content_type, "content": content},
	)
	try:
		activity = finergy.get_doc("Course Activity", activity[0]["name"])
	except (IndexError, finergy.DoesNotExistError):
		activity = finergy.get_doc(
			{
				"doctype": "Course Activity",
				"enrollment": enrollment,
				"content_type": content_type,
				"content": content,
				"activity_date": finergy.utils.datetime.datetime.now(),
			}
		).insert()
	return activity
