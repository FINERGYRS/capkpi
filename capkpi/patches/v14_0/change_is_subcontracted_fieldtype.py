# Copyright (c) 2022, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		finergy.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null""".format(
				doctype=doctype
			)
		)
		finergy.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'""".format(
				doctype=doctype
			)
		)

		finergy.reload_doc(finergy.get_meta(doctype).module, "doctype", finergy.scrub(doctype))
