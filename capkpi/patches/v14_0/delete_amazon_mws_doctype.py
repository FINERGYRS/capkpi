import finergy


def execute():
	finergy.delete_doc("DocType", "Amazon MWS Settings", ignore_missing=True)
