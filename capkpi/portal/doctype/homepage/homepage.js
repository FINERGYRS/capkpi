// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Homepage', {
	setup: function(frm) {
		frm.fields_dict["products"].grid.get_field("item").get_query = function() {
			return {
				filters: {'published': 1}
			}
		}
	},

	refresh: function(frm) {
		frm.add_custom_button(__('Set Meta Tags'), () => {
			finergy.utils.set_meta_tag('home');
		});
		frm.add_custom_button(__('Customize Homepage Sections'), () => {
			finergy.set_route('List', 'Homepage Section', 'List');
		});
	},
});

finergy.ui.form.on('Homepage Featured Product', {
	view: function(frm, cdt, cdn) {
		var child= locals[cdt][cdn];
		if (child.item_code && child.route) {
			window.open('/' + child.route, '_blank');
		}
	}
});
