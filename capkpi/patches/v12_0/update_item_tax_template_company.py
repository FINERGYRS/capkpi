import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "item_tax_template")

	item_tax_template_list = finergy.get_list("Item Tax Template")
	for template in item_tax_template_list:
		doc = finergy.get_doc("Item Tax Template", template.name)
		for tax in doc.taxes:
			doc.company = finergy.get_value("Account", tax.tax_type, "company")
			break
		doc.save()
