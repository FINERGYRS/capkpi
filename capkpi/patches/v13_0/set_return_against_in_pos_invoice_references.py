import finergy


def execute():
	"""
	Fetch and Set is_return & return_against from POS Invoice in POS Invoice References table.
	"""

	POSClosingEntry = finergy.qb.DocType("POS Closing Entry")
	open_pos_closing_entries = (
		finergy.qb.from_(POSClosingEntry)
		.select(POSClosingEntry.name)
		.where(POSClosingEntry.docstatus == 0)
		.run()
	)
	if open_pos_closing_entries:
		open_pos_closing_entries = [d[0] for d in open_pos_closing_entries]

	if not open_pos_closing_entries:
		return

	finergy.reload_doc("Accounts", "doctype", "pos_invoice_reference")

	POSInvoiceReference = finergy.qb.DocType("POS Invoice Reference")
	POSInvoice = finergy.qb.DocType("POS Invoice")
	pos_invoice_references = (
		finergy.qb.from_(POSInvoiceReference)
		.join(POSInvoice)
		.on(POSInvoiceReference.pos_invoice == POSInvoice.name)
		.select(POSInvoiceReference.name, POSInvoice.is_return, POSInvoice.return_against)
		.where(POSInvoiceReference.parent.isin(open_pos_closing_entries))
		.run(as_dict=True)
	)

	for row in pos_invoice_references:
		finergy.db.set_value("POS Invoice Reference", row.name, "is_return", row.is_return)
		if row.is_return:
			finergy.db.set_value("POS Invoice Reference", row.name, "return_against", row.return_against)
		else:
			finergy.db.set_value("POS Invoice Reference", row.name, "return_against", None)
