QUnit.module('hr');

QUnit.test("Test: Leave type [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	finergy.run_serially([
		// test leave type creation
		() => finergy.set_route("List", "Leave Type", "List"),
		() => finergy.new_doc("Leave Type"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("leave_type_name", "Test Leave type"),
		() => cur_frm.set_value("max_continuous_days_allowed", "5"),
		() => finergy.click_check('Is Carry Forward'),
		// save form
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => assert.equal("Test Leave type", cur_frm.doc.leave_type_name,
			'leave type correctly saved'),
		() => done()
	]);
});
