import finergy

from capkpi.regional.india.setup import add_permissions


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	finergy.reload_doc("regional", "doctype", "lower_deduction_certificate")
	finergy.reload_doc("regional", "doctype", "gstr_3b_report")
	add_permissions()
