QUnit.module('Payment Entry');

QUnit.test("test payment entry", function(assert) {
	assert.expect(8);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Sales Invoice', [
				{customer: 'Test Customer 1'},
				{company: 'For Testing'},
				{currency: 'INR'},
				{selling_price_list: '_Test Price List'},
				{items: [
					[
						{'qty': 1},
						{'item_code': 'Test Product 1'},
					]
				]}
			]);
		},
		() => finergy.timeout(1),
		() => cur_frm.save(),
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(1.5),
		() => finergy.click_button('Close'),
		() => finergy.timeout(0.5),
		() => finergy.click_button('Make'),
		() => finergy.timeout(1),
		() => finergy.click_link('Payment'),
		() => finergy.timeout(2),
		() => cur_frm.set_value("paid_to", "_Test Cash - FT"),
		() => finergy.timeout(0.5),
		() => {
			assert.equal(finergy.get_route()[1], 'Payment Entry', 'made payment entry');
			assert.equal(cur_frm.doc.party, 'Test Customer 1', 'customer set in payment entry');
			assert.equal(cur_frm.doc.paid_from, 'Debtors - FT', 'customer account set in payment entry');
			assert.equal(cur_frm.doc.paid_amount, 100, 'paid amount set in payment entry');
			assert.equal(cur_frm.doc.references[0].allocated_amount, 100,
				'amount allocated against sales invoice');
		},
		() => cur_frm.set_value('paid_amount', 95),
		() => finergy.timeout(1),
		() => {
			finergy.model.set_value("Payment Entry Reference",
				cur_frm.doc.references[0].name, "allocated_amount", 100);
		},
		() => finergy.timeout(.5),
		() => {
			assert.equal(cur_frm.doc.difference_amount, 5, 'difference amount is 5');
		},
		() => {
			finergy.db.set_value("Company", "For Testing", "write_off_account", "_Test Write Off - FT");
			finergy.timeout(1);
			finergy.db.set_value("Company", "For Testing",
				"exchange_gain_loss_account", "_Test Exchange Gain/Loss - FT");
		},
		() => finergy.timeout(1),
		() => finergy.click_button('Write Off Difference Amount'),
		() => finergy.timeout(2),
		() => {
			assert.equal(cur_frm.doc.difference_amount, 0, 'difference amount is zero');
			assert.equal(cur_frm.doc.deductions[0].amount, 5, 'Write off amount = 5');
		},
		() => done()
	]);
});
