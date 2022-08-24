# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import finergy

test_ignore = ["Leave Block List"]


class TestDepartment(unittest.TestCase):
	def test_remove_department_data(self):
		doc = create_department("Test Department")
		finergy.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None):
	doc = finergy.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": finergy.defaults.get_defaults().company,
		}
	).insert()

	return doc


test_records = finergy.get_test_records("Department")
