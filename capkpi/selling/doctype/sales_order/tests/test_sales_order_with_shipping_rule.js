QUnit.module('Sales Order');

QUnit.test("test sales order with shipping rule", function(assert) {
	assert.expect(2);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Sales Order', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'delivery_date': finergy.datetime.add_days(finergy.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 4'},
					]
				]},
				{customer_address: 'Test1-Billing'},
				{shipping_address_name: 'Test1-Shipping'},
				{contact_person: 'Contact 1-Test Customer 1'},
				{shipping_rule:'Next Day Shipping'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 4', "Item name correct");
			// get grand_total details
			assert.ok(cur_frm.doc.grand_total== 550, "Grand total correct ");
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
