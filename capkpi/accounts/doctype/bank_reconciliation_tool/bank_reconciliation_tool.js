// Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
finergy.provide("capkpi.accounts.bank_reconciliation");

finergy.ui.form.on("Bank Reconciliation Tool", {
	setup: function (frm) {
		frm.set_query("bank_account", function () {
			return {
				filters: {
					company: frm.doc.company,
					'is_company_account': 1
				},
			};
		});
	},

	onload: function (frm) {
		frm.trigger('bank_account');
	},

	refresh: function (frm) {
		finergy.require("bank-reconciliation-tool.bundle.js", () =>
			frm.trigger("make_reconciliation_tool")
		);
		frm.upload_statement_button = frm.page.set_secondary_action(
			__("Upload Bank Statement"),
			() =>
				finergy.call({
					method:
						"capkpi.accounts.doctype.bank_statement_import.bank_statement_import.upload_bank_statement",
					args: {
						dt: frm.doc.doctype,
						dn: frm.doc.name,
						company: frm.doc.company,
						bank_account: frm.doc.bank_account,
					},
					callback: function (r) {
						if (!r.exc) {
							var doc = finergy.model.sync(r.message);
							finergy.set_route(
								"Form",
								doc[0].doctype,
								doc[0].name
							);
						}
					},
				})
		);
	},

	after_save: function (frm) {
		frm.trigger("make_reconciliation_tool");
	},

	bank_account: function (frm) {
		finergy.db.get_value(
			"Bank Account",
			frm.doc.bank_account,
			"account",
			(r) => {
				finergy.db.get_value(
					"Account",
					r.account,
					"account_currency",
					(r) => {
						frm.currency = r.account_currency;
						frm.trigger("render_chart");
					}
				);
			}
		);
		frm.trigger("get_account_opening_balance");
	},

	bank_statement_from_date: function (frm) {
		frm.trigger("get_account_opening_balance");
	},

	make_reconciliation_tool(frm) {
		frm.get_field("reconciliation_tool_cards").$wrapper.empty();
		if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
			frm.trigger("get_cleared_balance").then(() => {
				if (
					frm.doc.bank_account &&
					frm.doc.bank_statement_from_date &&
					frm.doc.bank_statement_to_date
				) {
					frm.trigger("render_chart");
					frm.trigger("render");
					finergy.utils.scroll_to(
						frm.get_field("reconciliation_tool_cards").$wrapper,
						true,
						30
					);
				}
			});
		}
	},

	get_account_opening_balance(frm) {
		if (frm.doc.bank_account && frm.doc.bank_statement_from_date) {
			finergy.call({
				method:
					"capkpi.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: frm.doc.bank_account,
					till_date: frm.doc.bank_statement_from_date,
				},
				callback: (response) => {
					frm.set_value("account_opening_balance", response.message);
				},
			});
		}
	},

	get_cleared_balance(frm) {
		if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
			return finergy.call({
				method:
					"capkpi.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: frm.doc.bank_account,
					till_date: frm.doc.bank_statement_to_date,
				},
				callback: (response) => {
					frm.cleared_balance = response.message;
				},
			});
		}
	},

	render_chart: finergy.utils.debounce((frm) => {
		frm.cards_manager = new capkpi.accounts.bank_reconciliation.NumberCardManager(
			{
				$reconciliation_tool_cards: frm.get_field(
					"reconciliation_tool_cards"
				).$wrapper,
				bank_statement_closing_balance:
					frm.doc.bank_statement_closing_balance,
				cleared_balance: frm.cleared_balance,
				currency: frm.currency,
			}
		);
	}, 500),

	render(frm) {
		if (frm.doc.bank_account) {
			frm.bank_reconciliation_data_table_manager = new capkpi.accounts.bank_reconciliation.DataTableManager(
				{
					company: frm.doc.company,
					bank_account: frm.doc.bank_account,
					$reconciliation_tool_dt: frm.get_field(
						"reconciliation_tool_dt"
					).$wrapper,
					$no_bank_transactions: frm.get_field(
						"no_bank_transactions"
					).$wrapper,
					bank_statement_from_date: frm.doc.bank_statement_from_date,
					bank_statement_to_date: frm.doc.bank_statement_to_date,
					bank_statement_closing_balance:
						frm.doc.bank_statement_closing_balance,
					cards_manager: frm.cards_manager,
				}
			);
		}
	},
});
