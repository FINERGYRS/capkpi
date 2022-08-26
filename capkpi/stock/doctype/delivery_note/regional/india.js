{% include "capkpi/regional/india/taxes.js" %}

capkpi.setup_auto_gst_taxation('Delivery Note');

finergy.ui.form.on('Delivery Note', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && !frm.is_dirty() && !frm.doc.ewaybill) {
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
})