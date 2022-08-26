# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.utils import flt


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = finergy.get_doc(finergy.form_dict.doctype, finergy.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	context.parents = finergy.form_dict.parents
	context.title = finergy.form_dict.name

	if not finergy.has_website_permission(context.doc):
		finergy.throw(_("Not Permitted"), finergy.PermissionError)

	default_print_format = finergy.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=finergy.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"
	context.doc.items = get_more_items_info(context.doc.items, context.doc.name)


def get_more_items_info(items, material_request):
	for item in items:
		item.customer_provided = finergy.get_value("Item", item.item_code, "is_customer_provided_item")
		item.work_orders = finergy.db.sql(
			"""
			select
				wo.name, wo.status, wo_item.consumed_qty
			from
				`tabWork Order Item` wo_item, `tabWork Order` wo
			where
				wo_item.item_code=%s
				and wo_item.consumed_qty=0
				and wo_item.parent=wo.name
				and wo.status not in ('Completed', 'Cancelled', 'Stopped')
			order by
				wo.name asc""",
			item.item_code,
			as_dict=1,
		)
		item.delivered_qty = flt(
			finergy.db.sql(
				"""select sum(transfer_qty)
						from `tabStock Entry Detail` where material_request = %s
						and item_code = %s and docstatus = 1""",
				(material_request, item.item_code),
			)[0][0]
		)
	return items
