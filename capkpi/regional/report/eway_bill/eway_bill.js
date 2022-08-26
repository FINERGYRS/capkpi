// Copyright (c) 2016, FinByz Tech Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Eway Bill"] = {
	"filters": [
		{
			'fieldname': 'delivery_note',
			'label': __("Delivery Note"),
			'fieldtype': 'Link',
			'options': 'Delivery Note'
		},
		{
			'fieldname': 'posting_date',
			'label': __("Date"),
			'fieldtype': 'DateRange',
			'default': [finergy.datetime.nowdate(), finergy.datetime.nowdate()]
		},
		{
			'fieldname': 'customer',
			'label': __("Customer"),
			'fieldtype': 'Link',
			'options': 'Customer'
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": finergy.defaults.get_user_default("Company")
		},
	]
}
