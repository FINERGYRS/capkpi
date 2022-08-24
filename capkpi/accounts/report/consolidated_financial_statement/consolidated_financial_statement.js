// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.require("assets/capkpi/js/financial_statements.js", function() {
	finergy.query_reports["Consolidated Financial Statement"] = {
		"filters": [
			{
				"fieldname":"company",
				"label": __("Company"),
				"fieldtype": "Link",
				"options": "Company",
				"default": finergy.defaults.get_user_default("Company"),
				"reqd": 1
			},
			{
				"fieldname":"filter_based_on",
				"label": __("Filter Based On"),
				"fieldtype": "Select",
				"options": ["Fiscal Year", "Date Range"],
				"default": ["Fiscal Year"],
				"reqd": 1,
				on_change: function() {
					let filter_based_on = finergy.query_report.get_filter_value('filter_based_on');
					finergy.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
					finergy.query_report.toggle_filter_display('to_fiscal_year', filter_based_on === 'Date Range');
					finergy.query_report.toggle_filter_display('period_start_date', filter_based_on === 'Fiscal Year');
					finergy.query_report.toggle_filter_display('period_end_date', filter_based_on === 'Fiscal Year');

					finergy.query_report.refresh();
				}
			},
			{
				"fieldname":"period_start_date",
				"label": __("Start Date"),
				"fieldtype": "Date",
				"hidden": 1,
				"reqd": 1
			},
			{
				"fieldname":"period_end_date",
				"label": __("End Date"),
				"fieldtype": "Date",
				"hidden": 1,
				"reqd": 1
			},
			{
				"fieldname":"from_fiscal_year",
				"label": __("Start Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": finergy.defaults.get_user_default("fiscal_year"),
				"reqd": 1,
				on_change: () => {
					finergy.model.with_doc("Fiscal Year", finergy.query_report.get_filter_value('from_fiscal_year'), function(r) {
						let year_start_date = finergy.model.get_value("Fiscal Year", finergy.query_report.get_filter_value('from_fiscal_year'), "year_start_date");
						finergy.query_report.set_filter_value({
							period_start_date: year_start_date
						});
					});
				}
			},
			{
				"fieldname":"to_fiscal_year",
				"label": __("End Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": finergy.defaults.get_user_default("fiscal_year"),
				"reqd": 1,
				on_change: () => {
					finergy.model.with_doc("Fiscal Year", finergy.query_report.get_filter_value('to_fiscal_year'), function(r) {
						let year_end_date = finergy.model.get_value("Fiscal Year", finergy.query_report.get_filter_value('to_fiscal_year'), "year_end_date");
						finergy.query_report.set_filter_value({
							period_end_date: year_end_date
						});
					});
				}
			},
			{
				"fieldname":"finance_book",
				"label": __("Finance Book"),
				"fieldtype": "Link",
				"options": "Finance Book"
			},
			{
				"fieldname":"report",
				"label": __("Report"),
				"fieldtype": "Select",
				"options": ["Profit and Loss Statement", "Balance Sheet", "Cash Flow"],
				"default": "Balance Sheet",
				"reqd": 1
			},
			{
				"fieldname": "presentation_currency",
				"label": __("Currency"),
				"fieldtype": "Select",
				"options": capkpi.get_presentation_currency_list(),
				"default": finergy.defaults.get_user_default("Currency")
			},
			{
				"fieldname":"accumulated_in_group_company",
				"label": __("Accumulated Values in Group Company"),
				"fieldtype": "Check",
				"default": 0
			},
			{
				"fieldname": "include_default_book_entries",
				"label": __("Include Default Book Entries"),
				"fieldtype": "Check",
				"default": 1
			},
			{
				"fieldname": "show_zero_values",
				"label": __("Show zero values"),
				"fieldtype": "Check"
			}
		],
		"formatter": function(value, row, column, data, default_formatter) {
			if (data && column.fieldname=="account") {
				value = data.account_name || value;

				column.link_onclick =
				"capkpi.financial_statements.open_general_ledger(" + JSON.stringify(data) + ")";
				column.is_tree = true;
			}

			if (data && data.account && column.apply_currency_formatter) {
				data.currency = capkpi.get_currency(column.company_name);
			}

			value = default_formatter(value, row, column, data);
			if (!data.parent_account) {
				value = $(`<span>${value}</span>`);

				var $value = $(value).css("font-weight", "bold");

				value = $value.wrap("<p></p>").parent().html();
			}
			return value;
		},
		onload: function() {
			let fiscal_year = finergy.defaults.get_user_default("fiscal_year")

			finergy.model.with_doc("Fiscal Year", fiscal_year, function(r) {
				var fy = finergy.model.get_doc("Fiscal Year", fiscal_year);
				finergy.query_report.set_filter_value({
					period_start_date: fy.year_start_date,
					period_end_date: fy.year_end_date
				});
			});
		}
	}
});
