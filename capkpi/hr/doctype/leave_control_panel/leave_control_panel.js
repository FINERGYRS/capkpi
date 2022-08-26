// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.ui.form.on("Leave Control Panel", {
	onload: function(frm) {
		if (!frm.doc.from_date) {
			frm.set_value('from_date', finergy.datetime.get_today());
		}
	},
	refresh: function(frm) {
		frm.disable_save();
	},
	company: function(frm) {
		if(frm.doc.company) {
			frm.set_query("department", function() {
				return {
					"filters": {
						"company": frm.doc.company,
					}
				};
			});
		}
	}
});
