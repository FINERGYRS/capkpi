import finergy


def execute():
	install_apps = finergy.get_installed_apps()
	if "capkpi_datev_uo" in install_apps or "capkpi_datev" in install_apps:
		return

	# doctypes
	finergy.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	finergy.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
