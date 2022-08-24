// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Incorrect Balance Qty After Transaction"] = {
	"filters": [
		{
			label: __("Company"),
			fieldtype: "Link",
			fieldname: "company",
			options: "Company",
			default: finergy.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			label: __('Item Code'),
			fieldtype: 'Link',
			fieldname: 'item_code',
			options: 'Item'
		},
		{
			label: __('Warehouse'),
			fieldtype: 'Link',
			fieldname: 'warehouse'
		}
	]
};
