# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.exists("Company", {"country": "India"}):
		return

	finergy.reload_doc("core", "doctype", "has_role")
	finergy.db.sql(
		"""
		delete from
			`tabHas Role`
		where
			parenttype = 'Report' and parent in('GST Sales Register',
				'GST Purchase Register', 'GST Itemised Sales Register',
				'GST Itemised Purchase Register', 'Eway Bill')
		"""
	)
