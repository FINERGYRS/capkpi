# Copyright (c) 2020, Finergy and Contributors
# License: GNU General Public License v3. See license.txt

import finergy


def execute():
	count = finergy.db.sql(
		"SELECT COUNT(*) FROM `tabSingles` WHERE doctype='Amazon MWS Settings' AND field='enable_sync';"
	)[0][0]
	if count == 0:
		finergy.db.sql(
			"UPDATE `tabSingles` SET field='enable_sync' WHERE doctype='Amazon MWS Settings' AND field='enable_synch';"
		)

	finergy.reload_doc("CapKPI Integrations", "doctype", "Amazon MWS Settings")
