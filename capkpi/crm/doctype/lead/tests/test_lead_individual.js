QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(4);
	let done = assert.async();
	let lead_name = finergy.utils.get_random(10);
	finergy.run_serially([
		// test lead creation
		() => finergy.set_route("List", "Lead"),
		() => finergy.new_doc("Lead"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("lead_name", lead_name),
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => {
			assert.ok(cur_frm.doc.lead_name.includes(lead_name),
				'name correctly set');
			finergy.lead_name = cur_frm.doc.name;
		},
		// create address and contact
		() => finergy.click_link('Address & Contact'),
		() => finergy.click_button('New Address'),
		() => finergy.timeout(1),
		() => finergy.set_control('address_line1', 'Gateway'),
		() => finergy.set_control('city', 'Mumbai'),
		() => cur_frm.save(),
		() => finergy.timeout(3),
		() => assert.equal(finergy.get_route()[1], 'Lead',
			'back to lead form'),
		() => finergy.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('Mumbai'),
			'city is seen in address box'),

		// make opportunity
		() => finergy.click_button('Make'),
		() => finergy.click_link('Opportunity'),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.lead, finergy.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
