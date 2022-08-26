import finergy
from finergy import _


def execute():
	"""assign lft and rgt appropriately"""
	if "Healthcare" not in finergy.get_active_domains():
		return

	finergy.reload_doc("healthcare", "doctype", "healthcare_service_unit")
	finergy.reload_doc("healthcare", "doctype", "healthcare_service_unit_type")
	company = finergy.get_value("Company", {"domain": "Healthcare"}, "name")

	if company:
		finergy.get_doc(
			{
				"doctype": "Healthcare Service Unit",
				"healthcare_service_unit_name": _("All Healthcare Service Units"),
				"is_group": 1,
				"company": company,
			}
		).insert(ignore_permissions=True)
