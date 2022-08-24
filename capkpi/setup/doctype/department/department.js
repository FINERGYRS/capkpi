// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on("Department", {
	onload: function(frm) {
		frm.set_query("parent_department", function() {
			return {"filters": [["Department", "is_group", "=", 1]]};
		});
	},
	refresh: function(frm) {
		// read-only for root department
		if(!frm.doc.parent_department && !frm.is_new()) {
			frm.set_read_only();
			frm.set_intro(__("This is a root department and cannot be edited."));
		}
	},
	validate: function(frm) {
		if(frm.doc.name=="All Departments") {
			finergy.throw(__("You cannot edit root node."));
		}
	}
});
