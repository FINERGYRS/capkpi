QUnit.module('Buying');

QUnit.test("test: supplier quotation with item wise discount", function(assert){
	assert.expect(2);
	let done = assert.async();

	finergy.run_serially([
		() => {
			return finergy.tests.make('Supplier Quotation', [
				{supplier: 'Test Supplier'},
				{company: 'For Testing'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"warehouse": 'All Warehouses - FT'},
						{'discount_percentage': 10},
					]
				]}
			]);
		},

		() => {
			assert.ok(cur_frm.doc.total == 900, "Total correct");
			assert.ok(cur_frm.doc.grand_total == 900, "Grand total correct");
		},

		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
