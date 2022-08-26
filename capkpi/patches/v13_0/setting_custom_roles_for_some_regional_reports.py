import finergy

from capkpi.regional.india.setup import add_custom_roles_for_reports


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	add_custom_roles_for_reports()
