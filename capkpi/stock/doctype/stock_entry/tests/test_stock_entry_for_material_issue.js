QUnit.module('Stock');

QUnit.test("test material request", function(assert) {
	assert.expect(2);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Stock Entry', [
				{from_warehouse:'Stores - '+finergy.get_abbr(finergy.defaults.get_default('Company'))},
				{items: [
					[
						{'item_code': 'Test Product 1'},
						{'qty': 5},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => finergy.click_button('Update Rate and Availability'),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.total_outgoing_value==500, " Outgoing Value correct");
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
