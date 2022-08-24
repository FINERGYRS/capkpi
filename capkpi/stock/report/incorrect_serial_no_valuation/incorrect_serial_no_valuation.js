// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Incorrect Serial No Valuation"] = {
	"filters": [
		{
			label: __('Item Code'),
			fieldtype: 'Link',
			fieldname: 'item_code',
			options: 'Item',
			get_query: function() {
				return {
					filters: {
						'has_serial_no': 1
					}
				}
			}
		},
		{
			label: __('From Date'),
			fieldtype: 'Date',
			fieldname: 'from_date',
			reqd: 1,
			default: finergy.defaults.get_user_default("year_start_date")
		},
		{
			label: __('To Date'),
			fieldtype: 'Date',
			fieldname: 'to_date',
			reqd: 1,
			default: finergy.defaults.get_user_default("year_end_date")
		}
	]
};
