import finergy


def execute():
	if finergy.db.has_table("Tax Withholding Category") and finergy.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		finergy.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
