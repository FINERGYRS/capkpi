QUnit.module('Stock');

QUnit.test("test material request for transfer", function(assert) {
	assert.expect(1);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Material Request', [
				{material_request_type:'Manufacture'},
				{items: [
					[
						{'schedule_date':  finergy.datetime.add_days(finergy.datetime.nowdate(), 5)},
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
