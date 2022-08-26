QUnit.module('hr');

QUnit.test("Test: Employment type [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	finergy.run_serially([
		// test employment type creation
		() => finergy.set_route("List", "Employment Type", "List"),
		() => finergy.new_doc("Employment Type"),
		() => finergy.timeout(1),
		() => finergy.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => finergy.timeout(1),
		() => cur_frm.set_value("employee_type_name", "Test Employment type"),
		// save form
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => assert.equal("Test Employment type", cur_frm.doc.employee_type_name,
			'name of employment type correctly saved'),
		() => done()
	]);
});
