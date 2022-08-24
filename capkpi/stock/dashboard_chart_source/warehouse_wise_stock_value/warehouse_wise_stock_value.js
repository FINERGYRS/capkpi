finergy.provide('finergy.dashboards.chart_sources');

finergy.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "capkpi.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: finergy.defaults.get_user_default("Company")
		}
	]
};
