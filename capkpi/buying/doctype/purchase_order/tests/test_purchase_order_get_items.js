QUnit.module('Buying');

QUnit.test("test: purchase order with get items", function(assert) {
	assert.expect(4);
	let done = assert.async();

	finergy.run_serially([
		() => {
			return finergy.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-USD'},
				{currency: 'USD'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"schedule_date": finergy.datetime.add_days(finergy.datetime.now_date(), 1)},
						{"expected_delivery_date": finergy.datetime.add_days(finergy.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company"))}
					]
				]}
			]);
		},

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
		},

		() => finergy.timeout(0.3),
		() => finergy.click_button('Get items from'),
		() => finergy.timeout(0.3),

		() => finergy.click_link('Product Bundle'),
		() => finergy.timeout(0.5),

		() => cur_dialog.set_value('product_bundle', 'Computer'),
		() => finergy.click_button('Get Items'),
		() => finergy.timeout(1),

		// Check if items are fetched from Product Bundle
		() => {
			assert.ok(cur_frm.doc.items[1].item_name == 'CPU', "Product bundle item 1 correct");
			assert.ok(cur_frm.doc.items[2].item_name == 'Screen', "Product bundle item 2 correct");
			assert.ok(cur_frm.doc.items[3].item_name == 'Keyboard', "Product bundle item 3 correct");
		},

		() => cur_frm.doc.items[1].warehouse = 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company")),
		() => cur_frm.doc.items[2].warehouse = 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company")),
		() => cur_frm.doc.items[3].warehouse = 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company")),

		() => cur_frm.save(),
		() => finergy.timeout(1),

		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),

		() => done()
	]);
});
