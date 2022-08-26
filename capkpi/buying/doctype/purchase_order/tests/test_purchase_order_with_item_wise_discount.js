QUnit.module('Buying');

QUnit.test("test: purchase order with item wise discount", function(assert) {
	assert.expect(4);
	let done = assert.async();

	finergy.run_serially([
		() => {
			return finergy.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-EUR'},
				{currency: 'EUR'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"schedule_date": finergy.datetime.add_days(finergy.datetime.now_date(), 1)},
						{"expected_delivery_date": finergy.datetime.add_days(finergy.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company"))},
						{"discount_percentage": 20}
					]
				]}
			]);
		},

		() => finergy.timeout(1),

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].discount_percentage == 20, "Discount correct");
			// Calculate totals after discount
			assert.ok(cur_frm.doc.total == 2000, "Total correct");
			assert.ok(cur_frm.doc.grand_total == 2000, "Grand total correct");
		},

		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),

		() => done()
	]);
});
