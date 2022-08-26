QUnit.module('Pricing Rule');

QUnit.test("test pricing rule with different currency", function(assert) {
	assert.expect(3);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make("Pricing Rule", [
				{title: 'Test Pricing Rule 2'},
				{apply_on: 'Item Code'},
				{item_code:'Test Product 4'},
				{selling:1},
				{priority: 1},
				{min_qty:1},
				{max_qty:20},
				{valid_upto: finergy.datetime.add_days(finergy.defaults.get_default("year_end_date"), 1)},
				{margin_type: 'Amount'},
				{margin_rate_or_amount: 20},
				{rate_or_discount: 'Rate'},
				{rate:200},
				{currency:'USD'}

			]);
		},
		() => cur_frm.save(),
		() => finergy.timeout(0.3),
		() => {
			assert.ok(cur_frm.doc.item_code=='Test Product 4');
		},

		() => {
			return finergy.tests.make('Sales Order', [
				{customer: 'Test Customer 1'},
				{currency: 'INR'},
				{items: [
					[
						{'delivery_date': finergy.datetime.add_days(finergy.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': "Test Product 4"}
					]
				]}
			]);
		},
		() => cur_frm.save(),
		() => finergy.timeout(0.3),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].pricing_rule=='Test Pricing Rule 2', "Pricing rule correct");
			// margin not applied because different currency in pricing rule
			assert.ok(cur_frm.doc.items[0].margin_type==null, "Margin correct");
		},
		() => finergy.timeout(0.3),
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
