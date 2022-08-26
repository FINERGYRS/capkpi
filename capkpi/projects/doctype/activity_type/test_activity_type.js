QUnit.test("test: Activity Type", function (assert) {
	// number of asserts
	assert.expect(1);
	let done = assert.async();

	finergy.run_serially([
		// insert a new Activity Type
		() => finergy.set_route("List", "Activity Type", "List"),
		() => finergy.new_doc("Activity Type"),
		() => finergy.timeout(1),
		() => finergy.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => finergy.timeout(1),
		() => cur_frm.set_value("activity_type", "Test Activity"),
		() => finergy.click_button('Save'),
		() => finergy.timeout(1),
		() => {
			assert.equal(cur_frm.doc.name,"Test Activity");
		},
		() => done()
	]);
});
