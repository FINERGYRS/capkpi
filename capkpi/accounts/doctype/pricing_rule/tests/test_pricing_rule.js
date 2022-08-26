QUnit.module('Pricing Rule');

QUnit.test("test pricing rule", function(assert) {
	assert.expect(2);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make("Pricing Rule", [
				{title: 'Test Pricing Rule'},
				{item_code:'Test Product 2'},
				{selling:1},
				{applicable_for:'Customer'},
				{customer:'Test Customer 3'},
				{currency: finergy.defaults.get_default("currency")}
				{min_qty:1},
				{max_qty:20},
				{valid_upto: finergy.datetime.add_days(finergy.defaults.get_default("year_end_date"), 1)},
				{discount_percentage:10},
				{for_price_list:'Standard Selling'}
			]);
		},
		() => {
			assert.ok(cur_frm.doc.item_code=='Test Product 2');
			assert.ok(cur_frm.doc.customer=='Test Customer 3');
		},
		() => done()
	]);
});
