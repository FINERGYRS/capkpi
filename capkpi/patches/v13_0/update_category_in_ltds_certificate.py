import finergy


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	finergy.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = finergy.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = finergy.qb.DocType("Supplier")

	finergy.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
