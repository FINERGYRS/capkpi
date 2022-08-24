# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import finergy

# test_records = finergy.get_test_records('Designation')


def create_designation(**args):
	args = finergy._dict(args)
	if finergy.db.exists("Designation", args.designation_name or "_Test designation"):
		return finergy.get_doc("Designation", args.designation_name or "_Test designation")

	designation = finergy.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
