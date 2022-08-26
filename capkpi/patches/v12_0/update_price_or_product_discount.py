import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "pricing_rule")

	finergy.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
