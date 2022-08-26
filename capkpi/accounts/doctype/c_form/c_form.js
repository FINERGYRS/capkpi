// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

//c-form js file
// -----------------------------

finergy.ui.form.on('C-Form', {
	setup(frm) {
		frm.fields_dict.invoices.grid.get_field("invoice_no").get_query = function(doc) {
			return {
				filters: {
					"docstatus": 1,
					"customer": doc.customer,
					"company": doc.company,
					"c_form_applicable": 'Yes',
					"c_form_no": ''
				}
			};
		}

		frm.fields_dict.state.get_query = function() {
			return {
				filters: {
					country: "India"
				}
			};
		}
	}
});

finergy.ui.form.on('C-Form Invoice Detail', {
	invoice_no(frm, cdt, cdn) {
		let d = finergy.get_doc(cdt, cdn);

		if (d.invoice_no) {
			frm.call('get_invoice_details', {
				invoice_no: d.invoice_no
			}).then(r => {
				finergy.model.set_value(cdt, cdn, r.message);
			});
		}
	}
});
