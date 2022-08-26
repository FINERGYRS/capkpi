QUnit.module('hr');

QUnit.test("Test: Leave allocation [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	let today_date = finergy.datetime.nowdate();

	finergy.run_serially([
		// test creating leave alloction
		() => finergy.set_route("List", "Leave Allocation", "List"),
		() => finergy.new_doc("Leave Allocation"),
		() => finergy.timeout(1),
		() => {
			finergy.db.get_value('Employee', {'employee_name':'Test Employee 1'}, 'name', function(r) {
				cur_frm.set_value("employee", r.name)
			});
		},
		() => finergy.timeout(1),
		() => cur_frm.set_value("leave_type", "Test Leave type"),
		() => cur_frm.set_value("to_date", finergy.datetime.add_months(today_date, 2)),	// for two months
		() => cur_frm.set_value("description", "This is just for testing"),
		() => cur_frm.set_value("new_leaves_allocated", 2),
		() => finergy.click_check('Add unused leaves from previous allocations'),
		// save form
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => cur_frm.savesubmit(),
		() => finergy.timeout(1),
		() => assert.equal("Confirm", cur_dialog.title,
			'confirmation for leave alloction shown'),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(1),
		// check auto filled from date
		() => assert.equal(today_date, cur_frm.doc.from_date,
			"from date correctly set"),
		// check for total leaves
		() => assert.equal(cur_frm.doc.unused_leaves + 2, cur_frm.doc.total_leaves_allocated,
			"total leave calculation is correctly set"),
		() => done()
	]);
});
