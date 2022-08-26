QUnit.module('Sales Invoice');

QUnit.test("test sales Invoice with payment", function(assert) {
	assert.expect(4);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Sales Invoice', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					]
				]},
				{update_stock:1},
				{customer_address: 'Test1-Billing'},
				{shipping_address_name: 'Test1-Shipping'},
				{contact_person: 'Contact 1-Test Customer 1'},
				{taxes_and_charges: 'TEST In State GST - FT'},
				{tc_name: 'Test Term 1'},
				{terms: 'This is Test'},
				{payment_terms_template: '_Test Payment Term Template UI'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			// get tax details
			assert.ok(cur_frm.doc.taxes_and_charges=='TEST In State GST - FT', "Tax details correct");
			// grand_total Calculated
			assert.ok(cur_frm.doc.grand_total==590, "Grad Total correct");

		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(2),
		() => finergy.tests.click_button('Close'),
		() => finergy.tests.click_button('Make'),
		() => finergy.tests.click_link('Payment'),
		() => finergy.timeout(0.2),
		() => { cur_frm.set_value('mode_of_payment','Cash');},
		() => { cur_frm.set_value('paid_to','Cash - '+finergy.get_abbr(finergy.defaults.get_default('Company')));},
		() => {cur_frm.set_value('reference_no','TEST1234');},
		() => {cur_frm.set_value('reference_date',finergy.datetime.add_days(finergy.datetime.nowdate(), 0));},
		() => cur_frm.save(),
		() => {
			// get payment details
			assert.ok(cur_frm.doc.paid_amount==590, "Paid Amount Correct");
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => done()
	]);
});
