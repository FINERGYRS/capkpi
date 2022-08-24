import finergy

from capkpi.regional.united_states.setup import make_custom_fields


def execute():
	company = finergy.get_all("Company", filters={"country": "United States"})
	if not company:
		return

	make_custom_fields()
