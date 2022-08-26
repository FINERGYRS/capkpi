// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Donor', {
	refresh: function(frm) {
		finergy.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Donor'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			finergy.contacts.render_address_and_contact(frm);
		} else {
			finergy.contacts.clear_address_and_contact(frm);
		}

	}
});
