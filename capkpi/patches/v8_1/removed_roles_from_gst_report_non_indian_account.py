# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("core", "doctype", "has_role")
	company = finergy.get_all("Company", filters={"country": "India"})

	if not company:
		finergy.db.sql(
			"""
			delete from
				`tabHas Role`
			where
				parenttype = 'Report' and parent in('GST Sales Register',
					'GST Purchase Register', 'GST Itemised Sales Register',
					'GST Itemised Purchase Register', 'Eway Bill')"""
		)
