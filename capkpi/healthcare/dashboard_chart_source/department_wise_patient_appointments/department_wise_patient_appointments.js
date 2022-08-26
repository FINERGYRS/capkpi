finergy.provide('finergy.dashboards.chart_sources');

finergy.dashboards.chart_sources["Department wise Patient Appointments"] = {
	method: "capkpi.healthcare.dashboard_chart_source.department_wise_patient_appointments.department_wise_patient_appointments.get",
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
