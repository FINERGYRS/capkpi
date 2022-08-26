QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let lead_name = finergy.utils.get_random(10);
	finergy.run_serially([
		// test lead creation
		() => finergy.set_route("List", "Lead"),
		() => finergy.new_doc("Lead"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("organization_lead", "1"),
		() => cur_frm.set_value("company_name", lead_name),
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

		() => finergy.click_button('New Contact'),
		() => finergy.timeout(1),
		() => finergy.set_control('first_name', 'John'),
		() => finergy.set_control('last_name', 'Doe'),
		() => cur_frm.save(),
		() => finergy.timeout(3),
		() => finergy.set_route('Form', 'Lead', cur_frm.doc.links[0].link_name),
		() => finergy.timeout(1),
		() => finergy.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('John'),
			'contact is seen in contact box'),

		// make customer
		() => finergy.click_button('Make'),
		() => finergy.click_link('Customer'),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.lead_name, finergy.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
