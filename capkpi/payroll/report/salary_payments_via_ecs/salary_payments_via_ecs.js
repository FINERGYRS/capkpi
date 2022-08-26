// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.require("assets/capkpi/js/salary_slip_deductions_report_filters.js", function() {

	let ecs_checklist_filter = capkpi.salary_slip_deductions_report_filters
	ecs_checklist_filter['filters'].push({
		fieldname: "type",
		label: __("Type"),
		fieldtype: "Select",
		options:["", "Bank", "Cash", "Cheque"]
	})

	finergy.query_reports["Salary Payments via ECS"] = ecs_checklist_filter
});
