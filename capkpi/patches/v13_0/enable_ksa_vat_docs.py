import finergy

from capkpi.regional.saudi_arabia.setup import add_permissions, add_print_formats


def execute():
	company = finergy.get_all("Company", filters={"country": "Saudi Arabia"})
	if not company:
		return

	add_print_formats()
	add_permissions()
