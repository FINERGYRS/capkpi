// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Leave Policy', {
});

finergy.ui.form.on('Leave Policy Detail',{
	leave_type: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		if(child.leave_type){
			finergy.call({
				method: "finergy.client.get_value",
				args: {
					doctype: "Leave Type",
					fieldname: "max_leaves_allowed",
					filters: { name: child.leave_type }
				},
				callback: function(r) {
					if (r.message) {
						child.annual_allocation = r.message.max_leaves_allowed;
						refresh_field("leave_policy_details");
					}
				}
			});
		}
		else{
			child.annual_allocation = "";
			refresh_field("leave_policy_details");
		}
	}
});
