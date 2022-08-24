import finergy


def execute():

	doctypes = finergy.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		finergy.delete_doc("DocType", doctype, ignore_missing=True)

	finergy.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
