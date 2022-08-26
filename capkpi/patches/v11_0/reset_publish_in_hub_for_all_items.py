import finergy


def execute():
	finergy.reload_doc("stock", "doctype", "item")
	finergy.db.sql("""update `tabItem` set publish_in_hub = 0""")
