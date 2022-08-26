# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# MIT License. See license.txt


import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "Payment Schedule")
	if finergy.db.count("Payment Schedule"):
		finergy.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
