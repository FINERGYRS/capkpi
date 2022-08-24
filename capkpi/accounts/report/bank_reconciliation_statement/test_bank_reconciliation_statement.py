# Copyright (c) 2022, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.accounts.doctype.bank_transaction.test_bank_transaction import (
	create_loan_and_repayment,
)
from capkpi.accounts.report.bank_reconciliation_statement.bank_reconciliation_statement import (
	execute,
)
from capkpi.loan_management.doctype.loan.test_loan import create_loan_accounts


class TestBankReconciliationStatement(FinergyTestCase):
	def setUp(self):
		for dt in [
			"Loan Repayment",
			"Loan Disbursement",
			"Journal Entry",
			"Journal Entry Account",
			"Payment Entry",
		]:
			finergy.db.delete(dt)

	def test_loan_entries_in_bank_reco_statement(self):
		create_loan_accounts()
		repayment_entry = create_loan_and_repayment()

		filters = finergy._dict(
			{
				"company": "Test Company",
				"account": "Payment Account - _TC",
				"report_date": "2018-10-30",
			}
		)
		result = execute(filters)

		self.assertEqual(result[1][0].payment_entry, repayment_entry.name)
