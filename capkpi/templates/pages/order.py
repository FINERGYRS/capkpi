# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import finergy
from finergy import _

from capkpi.e_commerce.doctype.e_commerce_settings.e_commerce_settings import show_attachments


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = finergy.get_doc(finergy.form_dict.doctype, finergy.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	if show_attachments():
		context.attachments = get_attachments(finergy.form_dict.doctype, finergy.form_dict.name)

	context.parents = finergy.form_dict.parents
	context.title = finergy.form_dict.name
	context.payment_ref = finergy.db.get_value(
		"Payment Request", {"reference_name": finergy.form_dict.name}, "name"
	)

	context.enabled_checkout = finergy.get_doc("E Commerce Settings").enable_checkout

	default_print_format = finergy.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=finergy.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	if not finergy.has_website_permission(context.doc):
		finergy.throw(_("Not Permitted"), finergy.PermissionError)

	# check for the loyalty program of the customer
	customer_loyalty_program = finergy.db.get_value(
		"Customer", context.doc.customer, "loyalty_program"
	)
	if customer_loyalty_program:
		from capkpi.accounts.doctype.loyalty_program.loyalty_program import (
			get_loyalty_program_details_with_points,
		)

		loyalty_program_details = get_loyalty_program_details_with_points(
			context.doc.customer, customer_loyalty_program
		)
		context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))


def get_attachments(dt, dn):
	return finergy.get_all(
		"File",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)
