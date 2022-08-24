import finergy


def execute():
	finergy.reload_doctype("Employee")
	finergy.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	finergy.reload_doctype("Holiday List")
	for holiday_list in finergy.get_all("Holiday List"):
		holiday_list = finergy.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
