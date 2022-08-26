import finergy


def execute():
	finergy.reload_doctype("Pricing Rule")

	currency = finergy.db.get_default("currency")
	for doc in finergy.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = finergy.get_cached_value("Company", doc.company, "default_currency")

		finergy.db.sql(
			"""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name)
		)
