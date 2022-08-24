# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not finergy.db.table_exists(new_doc) and finergy.db.table_exists(old_doc):
			finergy.rename_doc("DocType", old_doc, new_doc)
			finergy.reload_doc("accounts", "doctype", finergy.scrub(new_doc))
			finergy.delete_doc("DocType", old_doc)
