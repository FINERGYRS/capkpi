import finergy
from finergy import _
from finergy.model.utils.rename_field import rename_field
from finergy.utils.nestedset import rebuild_tree


def execute():
	if finergy.db.table_exists("Supplier Group"):
		finergy.reload_doc("setup", "doctype", "supplier_group")
	elif finergy.db.table_exists("Supplier Type"):
		finergy.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		finergy.reload_doc("setup", "doctype", "supplier_group")
		finergy.reload_doc("accounts", "doctype", "pricing_rule")
		finergy.reload_doc("accounts", "doctype", "tax_rule")
		finergy.reload_doc("buying", "doctype", "buying_settings")
		finergy.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	finergy.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{0}'
		where is_group = 0""".format(
			_("All Supplier Groups")
		)
	)

	if not finergy.db.exists("Supplier Group", _("All Supplier Groups")):
		finergy.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group", "parent_supplier_group")
