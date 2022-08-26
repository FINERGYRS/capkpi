// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt


finergy.ui.form.on('Amazon MWS Settings', {
	refresh: function (frm) {
		let app_link = "<a href='https://github.com/finergyrs/ecommerce_integrations' target='_blank'>Ecommerce Integrations</a>"
		frm.dashboard.add_comment(__("Amazon MWS Integration will be removed from CapKPI in Version 14. Please install {0} app to continue using it.", [app_link]), "yellow", true);
	}
});
