# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy

import capkpi

test_dependencies = ["Employee", "Leave Type", "Leave Policy"]


class TestLeavePeriod(unittest.TestCase):
	pass


def create_leave_period(from_date, to_date, company=None):
	leave_period = finergy.db.get_value(
		"Leave Period",
		dict(
			company=company or capkpi.get_default_company(),
			from_date=from_date,
			to_date=to_date,
			is_active=1,
		),
		"name",
	)
	if leave_period:
		return finergy.get_doc("Leave Period", leave_period)

	leave_period = finergy.get_doc(
		{
			"doctype": "Leave Period",
			"company": company or capkpi.get_default_company(),
			"from_date": from_date,
			"to_date": to_date,
			"is_active": 1,
		}
	).insert()
	return leave_period
