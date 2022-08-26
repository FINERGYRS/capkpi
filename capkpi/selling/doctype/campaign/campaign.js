// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.ui.form.on("Campaign", "refresh", function(frm) {
	capkpi.toggle_naming_series();
	if(frm.doc.__islocal) {
		frm.toggle_display("naming_series", finergy.boot.sysdefaults.campaign_naming_by=="Naming Series");
	}
	else{
		cur_frm.add_custom_button(__("View Leads"), function() {
			finergy.route_options = {"source": "Campaign","campaign_name": frm.doc.name}
			finergy.set_route("List", "Lead");
		}, "fa fa-list", true);
	}
})
