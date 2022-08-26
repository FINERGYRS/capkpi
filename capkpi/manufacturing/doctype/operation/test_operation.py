# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy

test_records = finergy.get_test_records("Operation")


class TestOperation(unittest.TestCase):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = finergy._dict(args)

	if not finergy.db.exists("Operation", args.operation):
		doc = finergy.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return finergy.get_doc("Operation", args.operation)
