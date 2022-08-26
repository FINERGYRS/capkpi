// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Manufacturer', {
	refresh: function(frm) {
		finergy.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Manufacturer' };
		if (frm.doc.__islocal) {
			hide_field(['address_html','contact_html']);
			finergy.contacts.clear_address_and_contact(frm);
		}
		else {
			unhide_field(['address_html','contact_html']);
			finergy.contacts.render_address_and_contact(frm);
		}
	}
});
