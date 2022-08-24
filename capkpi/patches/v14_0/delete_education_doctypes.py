import click
import finergy


def execute():
	if "education" in finergy.get_installed_apps():
		return

	finergy.delete_doc("Workspace", "Education", ignore_missing=True, force=True)

	pages = finergy.get_all("Page", {"module": "education"}, pluck="name")
	for page in pages:
		finergy.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = finergy.get_all("Report", {"module": "education", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		finergy.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = finergy.get_all(
		"Print Format", {"module": "education", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		finergy.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	finergy.reload_doc("website", "doctype", "website_settings")
	forms = finergy.get_all("Web Form", {"module": "education", "is_standard": 1}, pluck="name")
	for form in forms:
		finergy.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = finergy.get_all("Dashboard", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		finergy.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = finergy.get_all(
		"Dashboard Chart", {"module": "education", "is_standard": 1}, pluck="name"
	)
	for dashboard in dashboards:
		finergy.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	finergy.reload_doc("desk", "doctype", "number_card")
	cards = finergy.get_all("Number Card", {"module": "education", "is_standard": 1}, pluck="name")
	for card in cards:
		finergy.delete_doc("Number Card", card, ignore_missing=True, force=True)

	doctypes = finergy.get_all("DocType", {"module": "education", "custom": 0}, pluck="name")
	for doctype in doctypes:
		finergy.delete_doc("DocType", doctype, ignore_missing=True)

	finergy.delete_doc("Module Def", "Education", ignore_missing=True, force=True)

	click.secho(
		"Education Module is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/FINERGYRS/education",
		fg="yellow",
	)
