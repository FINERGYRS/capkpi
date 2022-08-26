{% include "capkpi/regional/india/taxes.js" %}
{% include "capkpi/regional/india/e_invoice/einvoice.js" %}

capkpi.setup_auto_gst_taxation('Sales Invoice');
capkpi.setup_einvoice_actions('Sales Invoice')

finergy.ui.form.on("Sales Invoice", {
	setup: function(frm) {
		frm.set_query('transporter', function() {
			return {
				filters: {
					'is_transporter': 1
				}
			};
		});

		frm.set_query('driver', function(doc) {
			return {
				filters: {
					'transporter': doc.transporter
				}
			};
		});
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && !frm.is_dirty()
			&& !frm.doc.is_return && !frm.doc.ewaybill) {

			frm.add_custom_button('E-Way Bill JSON', () => {
				finergy.call({
					method: 'capkpi.regional.india.utils.generate_ewb_json',
					args: {
						'dt': frm.doc.doctype,
						'dn': [frm.doc.name]
					},
					callback: function(r) {
						if (r.message) {
							const args = {
								cmd: 'capkpi.regional.india.utils.download_ewb_json',
								data: r.message,
								docname: frm.doc.name
							};
							open_url_post(finergy.request.url, args);
						}
					}
				});

			}, __("Create"));
		}
	}

});