import finergy

from capkpi.regional.india.setup import make_custom_fields


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	make_custom_fields()
