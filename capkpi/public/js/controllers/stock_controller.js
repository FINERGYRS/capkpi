// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.provide("capkpi.stock");

capkpi.stock.StockController = class StockController extends finergy.ui.form.Controller {
	onload() {
		// warehouse query if company
		if (this.frm.fields_dict.company) {
			this.setup_warehouse_query();
		}
	}

	setup_warehouse_query() {
		var me = this;
		capkpi.queries.setup_queries(this.frm, "Warehouse", function() {
			return capkpi.queries.warehouse(me.frm.doc);
		});
	}

	setup_posting_date_time_check() {
		// make posting date default and read only unless explictly checked
		finergy.ui.form.on(this.frm.doctype, 'set_posting_date_and_time_read_only', function(frm) {
			if(frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
				frm.set_df_property('posting_date', 'read_only', 0);
				frm.set_df_property('posting_time', 'read_only', 0);
			} else {
				frm.set_df_property('posting_date', 'read_only', 1);
				frm.set_df_property('posting_time', 'read_only', 1);
			}
		})

		finergy.ui.form.on(this.frm.doctype, 'set_posting_time', function(frm) {
			frm.trigger('set_posting_date_and_time_read_only');
		});

		finergy.ui.form.on(this.frm.doctype, 'refresh', function(frm) {
			// set default posting date / time
			if(frm.doc.docstatus==0) {
				if(!frm.doc.posting_date) {
					frm.set_value('posting_date', finergy.datetime.nowdate());
				}
				if(!frm.doc.posting_time) {
					frm.set_value('posting_time', finergy.datetime.now_time());
				}
				frm.trigger('set_posting_date_and_time_read_only');
			}
		});
	}

	show_stock_ledger() {
		var me = this;
		if(this.frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(__("Stock Ledger"), function() {
				finergy.route_options = {
					voucher_no: me.frm.doc.name,
					from_date: me.frm.doc.posting_date,
					to_date: moment(me.frm.doc.modified).format('YYYY-MM-DD'),
					company: me.frm.doc.company,
					show_cancelled_entries: me.frm.doc.docstatus === 2
				};
				finergy.set_route("query-report", "Stock Ledger");
			}, __("View"));
		}

	}

	show_general_ledger() {
		var me = this;
		if(this.frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(__('Accounting Ledger'), function() {
				finergy.route_options = {
					voucher_no: me.frm.doc.name,
					from_date: me.frm.doc.posting_date,
					to_date: moment(me.frm.doc.modified).format('YYYY-MM-DD'),
					company: me.frm.doc.company,
					group_by: "Group by Voucher (Consolidated)",
					show_cancelled_entries: me.frm.doc.docstatus === 2
				};
				finergy.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	}
};
