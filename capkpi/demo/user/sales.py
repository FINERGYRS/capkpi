# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import random

import finergy
from finergy.utils import flt
from finergy.utils.make_random import add_random_children, get_random

import capkpi
from capkpi.accounts.doctype.payment_request.payment_request import (
	make_payment_entry,
	make_payment_request,
)
from capkpi.accounts.party import get_party_account_currency
from capkpi.setup.utils import get_exchange_rate


def work(domain="Manufacturing"):
	finergy.set_user(finergy.db.get_global("demo_sales_user_2"))

	for i in range(random.randint(1, 7)):
		if random.random() < 0.5:
			make_opportunity(domain)

	for i in range(random.randint(1, 3)):
		if random.random() < 0.5:
			make_quotation(domain)

	try:
		lost_reason = finergy.get_doc(
			{"doctype": "Opportunity Lost Reason", "lost_reason": "Did not ask"}
		)
		lost_reason.save(ignore_permissions=True)
	except finergy.exceptions.DuplicateEntryError:
		pass

	# lost quotations / inquiries
	if random.random() < 0.3:
		for i in range(random.randint(1, 3)):
			quotation = get_random("Quotation", doc=True)
			if quotation and quotation.status == "Submitted":
				quotation.declare_order_lost([{"lost_reason": "Did not ask"}])

		for i in range(random.randint(1, 3)):
			opportunity = get_random("Opportunity", doc=True)
			if opportunity and opportunity.status in ("Open", "Replied"):
				opportunity.declare_enquiry_lost([{"lost_reason": "Did not ask"}])

	for i in range(random.randint(1, 3)):
		if random.random() < 0.6:
			make_sales_order()

	if random.random() < 0.5:
		# make payment request against Sales Order
		sales_order_name = get_random("Sales Order", filters={"docstatus": 1})
		try:
			if sales_order_name:
				so = finergy.get_doc("Sales Order", sales_order_name)
				if flt(so.per_billed) != 100:
					payment_request = make_payment_request(
						dt="Sales Order",
						dn=so.name,
						recipient_id=so.contact_email,
						submit_doc=True,
						mute_email=True,
						use_dummy_message=True,
					)

					payment_entry = finergy.get_doc(make_payment_entry(payment_request.name))
					payment_entry.posting_date = finergy.flags.current_date
					payment_entry.submit()
		except Exception:
			pass


def make_opportunity(domain):
	b = finergy.get_doc(
		{
			"doctype": "Opportunity",
			"opportunity_from": "Customer",
			"party_name": finergy.get_value("Customer", get_random("Customer"), "name"),
			"opportunity_type": "Sales",
			"with_items": 1,
			"transaction_date": finergy.flags.current_date,
		}
	)

	add_random_children(
		b,
		"items",
		rows=4,
		randomize={
			"qty": (1, 5),
			"item_code": ("Item", {"has_variants": 0, "is_fixed_asset": 0, "domain": domain}),
		},
		unique="item_code",
	)

	b.insert()
	finergy.db.commit()


def make_quotation(domain):
	# get open opportunites
	opportunity = get_random("Opportunity", {"status": "Open", "with_items": 1})

	if opportunity:
		from capkpi.crm.doctype.opportunity.opportunity import make_quotation

		qtn = finergy.get_doc(make_quotation(opportunity))
		qtn.insert()
		finergy.db.commit()
		qtn.submit()
		finergy.db.commit()
	else:
		# make new directly

		# get customer, currency and exchange_rate
		customer = get_random("Customer")

		company_currency = finergy.get_cached_value(
			"Company", capkpi.get_default_company(), "default_currency"
		)
		party_account_currency = get_party_account_currency(
			"Customer", customer, capkpi.get_default_company()
		)
		if company_currency == party_account_currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(party_account_currency, company_currency, args="for_selling")

		qtn = finergy.get_doc(
			{
				"creation": finergy.flags.current_date,
				"doctype": "Quotation",
				"quotation_to": "Customer",
				"party_name": customer,
				"currency": party_account_currency or company_currency,
				"conversion_rate": exchange_rate,
				"order_type": "Sales",
				"transaction_date": finergy.flags.current_date,
			}
		)

		add_random_children(
			qtn,
			"items",
			rows=3,
			randomize={
				"qty": (1, 5),
				"item_code": ("Item", {"has_variants": "0", "is_fixed_asset": 0, "domain": domain}),
			},
			unique="item_code",
		)

		qtn.insert()
		finergy.db.commit()
		qtn.submit()
		finergy.db.commit()


def make_sales_order():
	q = get_random("Quotation", {"status": "Submitted"})
	if q:
		from capkpi.selling.doctype.quotation.quotation import make_sales_order as mso

		so = finergy.get_doc(mso(q))
		so.transaction_date = finergy.flags.current_date
		so.delivery_date = finergy.utils.add_days(finergy.flags.current_date, 10)
		so.insert()
		finergy.db.commit()
		so.submit()
		finergy.db.commit()
