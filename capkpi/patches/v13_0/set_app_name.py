import finergy


def execute():
	finergy.reload_doctype("System Settings")
	settings = finergy.get_doc("System Settings")
	settings.db_set("app_name", "CapKPI", commit=True)
