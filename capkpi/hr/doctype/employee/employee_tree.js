finergy.treeview_settings['Employee'] = {
	get_tree_nodes: "capkpi.hr.doctype.employee.employee.get_children",
	filters: [
		{
			fieldname: "company",
			fieldtype:"Select",
			options: ['All Companies'].concat(capkpi.utils.get_tree_options("company")),
			label: __("Company"),
			default: capkpi.utils.get_tree_default("company")
		}
	],
	breadcrumb: "Hr",
	disable_add_node: true,
	get_tree_root: false,
	toolbar: [
		{ toggle_btn: true },
		{
			label:__("Edit"),
			condition: function(node) {
				return !node.is_root;
			},
			click: function(node) {
				finergy.set_route("Form", "Employee", node.data.value);
			}
		}
	],
	menu_items: [
		{
			label: __("New Employee"),
			action: function() {
				finergy.new_doc("Employee", true);
			},
			condition: 'finergy.boot.user.can_create.indexOf("Employee") !== -1'
		}
	],
};