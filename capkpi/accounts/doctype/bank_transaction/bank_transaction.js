// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on("Bank Transaction", {
	onload(frm) {
		frm.set_query("payment_document", "payment_entries", function () {
			return {
				filters: {
					name: [
						"in",
						[
							"Payment Entry",
							"Journal Entry",
							"Sales Invoice",
							"Purchase Invoice",
							"Expense Claim",
						],
					],
				},
			};
		});
	},
	bank_account: function (frm) {
		set_bank_statement_filter(frm);
	},

	setup: function (frm) {
		frm.set_query("party_type", function () {
			return {
				filters: {
					name: ["in", Object.keys(finergy.boot.party_account_types)],
				},
			};
		});
	},
});

finergy.ui.form.on("Bank Transaction Payments", {
	payment_entries_remove: function (frm, cdt, cdn) {
		update_clearance_date(frm, cdt, cdn);
	},
});

const update_clearance_date = (frm, cdt, cdn) => {
	if (frm.doc.docstatus === 1) {
		finergy
			.xcall(
				"capkpi.accounts.doctype.bank_transaction.bank_transaction.unclear_reference_payment",
				{ doctype: cdt, docname: cdn }
			)
			.then((e) => {
				if (e == "success") {
					finergy.show_alert({
						message: __("Document {0} successfully uncleared", [e]),
						indicator: "green",
					});
				}
			});
	}
};

function set_bank_statement_filter(frm) {
	frm.set_query("bank_statement", function () {
		return {
			filters: {
				bank_account: frm.doc.bank_account,
			},
		};
	});
}
