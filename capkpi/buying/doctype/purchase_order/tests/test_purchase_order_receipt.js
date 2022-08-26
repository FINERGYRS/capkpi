QUnit.module('Buying');

QUnit.test("test: purchase order receipt", function(assert) {
	assert.expect(5);
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
						{"item_code": 'Test Product 1'},
						{"schedule_date": finergy.datetime.add_days(finergy.datetime.now_date(), 1)},
						{"expected_delivery_date": finergy.datetime.add_days(finergy.datetime.now_date(), 5)},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"warehouse": 'Stores - '+finergy.get_abbr(finergy.defaults.get_default("Company"))}
					]
				]},
			]);
		},

		() => {

			// Check supplier and item details
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.items[0].description == 'Test Product 1', "Description correct");
			assert.ok(cur_frm.doc.items[0].qty == 5, "Quantity correct");

		},

		() => finergy.timeout(1),

		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),

		() => finergy.timeout(1.5),
		() => finergy.click_button('Close'),
		() => finergy.timeout(0.3),

		// Make Purchase Receipt
		() => finergy.click_button('Make'),
		() => finergy.timeout(0.3),

		() => finergy.click_link('Receipt'),
		() => finergy.timeout(2),

		() => cur_frm.save(),

		// Save and submit Purchase Receipt
		() => finergy.timeout(1),
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(1),

		// View Purchase order in Stock Ledger
		() => finergy.click_button('View'),
		() => finergy.timeout(0.3),

		() => finergy.click_link('Stock Ledger'),
		() => finergy.timeout(2),
		() => {
			assert.ok($('div.slick-cell.l2.r2 > a').text().includes('Test Product 1')
				&& $('div.slick-cell.l9.r9 > div').text().includes(5), "Stock ledger entry correct");
		},
		() => done()
	]);
});
