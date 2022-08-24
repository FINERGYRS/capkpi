import finergy


def execute():
	if "agriculture" in finergy.get_installed_apps():
		return

	finergy.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	finergy.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = finergy.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		finergy.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = finergy.get_all(
		"Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name"
	)
	for dashboard in dashboards:
		finergy.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = finergy.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		finergy.delete_doc("DocType", doctype, ignore_missing=True)

	finergy.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
