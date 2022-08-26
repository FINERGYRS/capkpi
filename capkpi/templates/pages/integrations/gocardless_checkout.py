# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import json

import finergy
from finergy import _
from finergy.utils import flt, get_url

from capkpi.capkpi_integrations.doctype.gocardless_settings.gocardless_settings import (
	get_gateway_controller,
	gocardless_initialization,
)

no_cache = 1

expected_keys = (
	"amount",
	"title",
	"description",
	"reference_doctype",
	"reference_docname",
	"payer_name",
	"payer_email",
	"order_id",
	"currency",
)


def get_context(context):
	context.no_cache = 1

	# all these keys exist in form_dict
	if not (set(expected_keys) - set(finergy.form_dict.keys())):
		for key in expected_keys:
			context[key] = finergy.form_dict[key]

		context["amount"] = flt(context["amount"])

		gateway_controller = get_gateway_controller(context.reference_docname)
		context["header_img"] = finergy.db.get_value(
			"GoCardless Settings", gateway_controller, "header_img"
		)

	else:
		finergy.redirect_to_message(
			_("Some information is missing"),
			_("Looks like someone sent you to an incomplete URL. Please ask them to look into it."),
		)
		finergy.local.flags.redirect_location = finergy.local.response.location
		raise finergy.Redirect


@finergy.whitelist(allow_guest=True)
def check_mandate(data, reference_doctype, reference_docname):
	data = json.loads(data)

	client = gocardless_initialization(reference_docname)

	payer = finergy.get_doc("Customer", data["payer_name"])

	if payer.customer_type == "Individual" and payer.customer_primary_contact is not None:
		primary_contact = finergy.get_doc("Contact", payer.customer_primary_contact)
		prefilled_customer = {
			"company_name": payer.name,
			"given_name": primary_contact.first_name,
		}
		if primary_contact.last_name is not None:
			prefilled_customer.update({"family_name": primary_contact.last_name})

		if primary_contact.email_id is not None:
			prefilled_customer.update({"email": primary_contact.email_id})
		else:
			prefilled_customer.update({"email": finergy.session.user})

	else:
		prefilled_customer = {"company_name": payer.name, "email": finergy.session.user}

	success_url = get_url(
		"./integrations/gocardless_confirmation?reference_doctype="
		+ reference_doctype
		+ "&reference_docname="
		+ reference_docname
	)

	try:
		redirect_flow = client.redirect_flows.create(
			params={
				"description": _("Pay {0} {1}").format(data["amount"], data["currency"]),
				"session_token": finergy.session.user,
				"success_redirect_url": success_url,
				"prefilled_customer": prefilled_customer,
			}
		)

		return {"redirect_to": redirect_flow.redirect_url}

	except Exception as e:
		finergy.log_error(e, "GoCardless Payment Error")
		return {"redirect_to": "/integrations/payment-failed"}
