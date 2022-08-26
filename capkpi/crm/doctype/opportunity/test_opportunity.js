QUnit.test("test: opportunity", function (assert) {
	assert.expect(8);
	let done = assert.async();
	finergy.run_serially([
		() => finergy.set_route('List', 'Opportunity'),
		() => finergy.timeout(1),
		() => finergy.click_button('New'),
		() => finergy.timeout(1),
		() => cur_frm.set_value('opportunity_from', 'Customer'),
		() => cur_frm.set_value('customer', 'Test Customer 1'),

		// check items
		() => cur_frm.set_value('with_items', 1),
		() => finergy.tests.set_grid_values(cur_frm, 'items', [
			[
				{item_code:'Test Product 1'},
				{qty: 4}
			]
		]),
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => {
			assert.notOk(cur_frm.is_new(), 'saved');
			finergy.opportunity_name = cur_frm.doc.name;
		},

		// close and re-open
		() => finergy.click_button('Close'),
		() => finergy.timeout(1),
		() => assert.equal(cur_frm.doc.status, 'Closed',
			'closed'),

		() => finergy.click_button('Reopen'),
		() => assert.equal(cur_frm.doc.status, 'Open',
			'reopened'),
		() => finergy.timeout(1),

		// make quotation
		() => finergy.click_button('Make'),
		() => finergy.click_link('Quotation', 1),
		() => finergy.timeout(2),
		() => {
			assert.equal(finergy.get_route()[1], 'Quotation',
				'made quotation');
			assert.equal(cur_frm.doc.customer, 'Test Customer 1',
				'customer set in quotation');
			assert.equal(cur_frm.doc.items[0].item_code, 'Test Product 1',
				'item set in quotation');
			assert.equal(cur_frm.doc.items[0].qty, 4,
				'qty set in quotation');
			assert.equal(cur_frm.doc.items[0].prevdoc_docname, finergy.opportunity_name,
				'opportunity set in quotation');
		},
		() => done()
	]);
});
