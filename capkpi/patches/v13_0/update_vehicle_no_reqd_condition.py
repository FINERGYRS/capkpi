import finergy


def execute():
	finergy.reload_doc("custom", "doctype", "custom_field", force=True)
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if finergy.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		finergy.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
