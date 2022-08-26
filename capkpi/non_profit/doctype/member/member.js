// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Member', {
	setup: function(frm) {
		finergy.db.get_single_value('Non Profit Settings', 'enable_razorpay_for_memberships').then(val => {
			if (val && (frm.doc.subscription_id || frm.doc.customer_id)) {
				frm.set_df_property('razorpay_details_section', 'hidden', false);
			}
		})
	},

	refresh: function(frm) {

		finergy.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Member'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			finergy.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function() {
				if (frm.doc.customer) {
					finergy.set_route('query-report', 'General Ledger', {party_type: 'Customer', party: frm.doc.customer});
				} else {
					finergy.set_route('query-report', 'General Ledger', {party_type: 'Member', party: frm.doc.name});
				}
			});

			if (frm.doc.customer) {
				frm.add_custom_button(__('Accounts Receivable'), function() {
					finergy.set_route('query-report', 'Accounts Receivable', {customer: frm.doc.customer});
				});
			}

			if (!frm.doc.customer) {
				frm.add_custom_button(__('Create Customer'), () => {
					frm.call('make_customer_and_link').then(() => {
						frm.reload_doc();
					});
				});
			}

			// indicator
			capkpi.utils.set_party_dashboard_indicators(frm);

		} else {
			finergy.contacts.clear_address_and_contact(frm);
		}

		if (!frm.doc.membership_expiry_date && !frm.doc.__islocal) {
			finergy.call({
				method: "capkpi.get_last_membership",
				args: {
					member: frm.doc.member
				},
				callback: function(data) {
					if (data.message) {
						finergy.model.set_value(frm.doctype, frm.docname, "membership_expiry_date", data.message.to_date);
					}
				}
			});
		}
	}
});