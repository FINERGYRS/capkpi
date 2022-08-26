import finergy


def execute():
	if finergy.db.exists("Page", "point-of-sale"):
		finergy.rename_doc("Page", "pos", "point-of-sale", 1, 1)
