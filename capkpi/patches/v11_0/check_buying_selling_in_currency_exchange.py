import finergy


def execute():
	finergy.reload_doc("setup", "doctype", "currency_exchange")
	finergy.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
