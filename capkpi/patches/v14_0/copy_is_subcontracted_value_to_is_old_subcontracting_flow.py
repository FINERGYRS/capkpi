# Copyright (c) 2022, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = finergy.qb.DocType(doctype).as_("tab")
		finergy.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(
			tab.is_subcontracted == 1
		).run()
