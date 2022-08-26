QUnit.module('buying');

QUnit.test("Test: Request for Quotation", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let rfq_name = "";

	finergy.run_serially([
		// Go to RFQ list
		() => finergy.set_route("List", "Request for Quotation"),
		// Create a new RFQ
		() => finergy.new_doc("Request for Quotation"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("transaction_date", "04-04-2017"),
		() => cur_frm.set_value("company", "For Testing"),
		// Add Suppliers
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => finergy.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.supplier = "_Test Supplier";
			finergy.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => finergy.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => finergy.timeout(1),
		() => finergy.click_button('Add Row',0),
		() => finergy.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].toggle_view();
		},
		() => finergy.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.supplier = "_Test Supplier 1";
			finergy.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => finergy.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => finergy.timeout(1),
		// Add Item
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].toggle_view();
		},
		() => finergy.timeout(1),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.item_code = "_Test Item";
			finergy.set_control('item_code',"_Test Item");
			finergy.set_control('qty',5);
			finergy.set_control('schedule_date', "05-05-2017");
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => finergy.timeout(2),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => finergy.timeout(2),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.warehouse = "_Test Warehouse - FT";
		},
		() => finergy.click_button('Save'),
		() => finergy.timeout(1),
		() => finergy.click_button('Submit'),
		() => finergy.timeout(1),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(1),
		() => finergy.click_button('Menu'),
		() => finergy.timeout(1),
		() => finergy.click_link('Reload'),
		() => finergy.timeout(1),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1);
			rfq_name = cur_frm.doc.name;
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.quote_status == "Pending");
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Pending");
		},
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => finergy.timeout(1),
		() => finergy.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => finergy.click_button('Update'),
		() => finergy.timeout(1),

		() => finergy.click_button('Supplier Quotation'),
		() => finergy.timeout(1),
		() => finergy.click_link('Make'),
		() => finergy.timeout(1),
		() => {
			finergy.set_control('supplier',"_Test Supplier 1");
		},
		() => finergy.timeout(1),
		() => finergy.click_button('Make Supplier Quotation'),
		() => finergy.timeout(1),
		() => cur_frm.set_value("company", "For Testing"),
		() => cur_frm.fields_dict.items.grid.grid_rows[0].doc.rate = 4.99,
		() => finergy.timeout(1),
		() => finergy.click_button('Save'),
		() => finergy.timeout(1),
		() => finergy.click_button('Submit'),
		() => finergy.timeout(1),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(1),
		() => finergy.set_route("List", "Request for Quotation"),
		() => finergy.timeout(2),
		() => finergy.set_route("List", "Request for Quotation"),
		() => finergy.timeout(2),
		() => finergy.click_link(rfq_name),
		() => finergy.timeout(1),
		() => finergy.click_button('Menu'),
		() => finergy.timeout(1),
		() => finergy.click_link('Reload'),
		() => finergy.timeout(1),
		() => {
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Received");
		},
		() => done()
	]);
});
