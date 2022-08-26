// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Shopify Log', {
	refresh: function(frm) {
		if (frm.doc.request_data && frm.doc.status=='Error'){
			frm.add_custom_button('Resync', function() {
				finergy.call({
					method:"capkpi.capkpi_integrations.doctype.shopify_log.shopify_log.resync",
					args:{
						method:frm.doc.method,
						name: frm.doc.name,
						request_data: frm.doc.request_data
					},
					callback: function(r){
						finergy.msgprint(__("Order rescheduled for sync"))
					}
				})
			}).addClass('btn-primary');
		}

	let app_link = "<a href='https://finergycloud.com/marketplace/apps/ecommerce-integrations' target='_blank'>Ecommerce Integrations</a>"
	frm.dashboard.add_comment(__("Shopify Integration will be removed from CapKPI in Version 14. Please install {0} app to continue using it.", [app_link]), "yellow", true);
	}
});