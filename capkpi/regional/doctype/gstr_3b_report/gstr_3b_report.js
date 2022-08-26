// Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('GSTR 3B Report', {
	refresh : function(frm) {
		frm.doc.__unsaved = 1;
		if(!frm.is_new()) {
			frm.set_intro(__("Please save the report again to rebuild or update"));
			frm.add_custom_button(__('Download JSON'), function() {
				var w = window.open(
					finergy.urllib.get_full_url(
						"/api/method/capkpi.regional.doctype.gstr_3b_report.gstr_3b_report.make_json?"
						+"name="+encodeURIComponent(frm.doc.name)));

				if(!w) {
					finergy.msgprint(__("Please enable pop-ups")); return;
				}
			});
			frm.add_custom_button(__('View Form'), function() {
				finergy.call({
					"method" : "capkpi.regional.doctype.gstr_3b_report.gstr_3b_report.view_report",
					"args" : {
						name : frm.doc.name,
					},
					"callback" : function(r){

						let data = r.message;

						finergy.ui.get_print_settings(false, print_settings => {

							finergy.render_grid({
								template: 'gstr_3b_report',
								title: __(this.doctype),
								print_settings: print_settings,
								data: data,
								columns:[]
							});
						});
					}
				});
			});
		}

		let current_year = new Date().getFullYear();
		let options = [current_year, current_year-1, current_year-2];
		frm.set_df_property('year', 'options', options);
	},

	setup: function(frm) {
		frm.set_query('company_address', function(doc) {
			if(!doc.company) {
				finergy.throw(__('Please set Company'));
			}

			return {
				query: 'finergy.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: doc.company
				}
			};
		});
	},
});
