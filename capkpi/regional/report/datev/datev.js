finergy.query_reports["DATEV"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": finergy.defaults.get_user_default("Company") || finergy.defaults.get_global_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"default": moment().subtract(1, 'month').startOf('month').format(),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"default": moment().subtract(1, 'month').endOf('month').format(),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "voucher_type",
			"label": __("Voucher Type"),
			"fieldtype": "Select",
			"options": "\nSales Invoice\nPurchase Invoice\nPayment Entry\nExpense Claim\nPayroll Entry\nBank Reconciliation\nAsset\nStock Entry"
		}
	],
	onload: function(query_report) {
		let company = finergy.query_report.get_filter_value('company');
		finergy.db.exists('DATEV Settings', company).then((settings_exist) => {
			if (!settings_exist) {
				finergy.confirm(__('DATEV Settings for your Company are missing. Would you like to create them now?'),
					() => finergy.new_doc('DATEV Settings', {'company': company})
				);
			}
		});

		query_report.page.add_menu_item(__("Download DATEV File"), () => {
			const filters = encodeURIComponent(
				JSON.stringify(
					query_report.get_values()
				)
			);
			window.open(`/api/method/capkpi.regional.report.datev.datev.download_datev_csv?filters=${filters}`);
		});

		query_report.page.add_menu_item(__("Change DATEV Settings"), () => {
			let company = finergy.query_report.get_filter_value('company'); // read company from filters again – it might have changed by now.
			finergy.set_route('Form', 'DATEV Settings', company);
		});
	}
};
