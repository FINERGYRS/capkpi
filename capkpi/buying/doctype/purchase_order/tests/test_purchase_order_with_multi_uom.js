QUnit.module('Buying');

QUnit.test("test: purchase order with multi UOM", function(assert) {
	assert.expect(3);
	let done = assert.async();

	finergy.run_serially([
		() => {
			return finergy.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"schedule_date": finergy.datetime.add_days(finergy.datetime.now_date(), 1)},
						{"expected_delivery_date": finergy.datetime.add_days(finergy.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company"))}
					]
				]}
			]);
		},

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 4', "Item name correct");
			assert.ok(cur_frm.doc.items[0].uom == 'Unit', "Multi UOM correct");
		},

		() => finergy.timeout(1),
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),

		() => done()
	]);
});
