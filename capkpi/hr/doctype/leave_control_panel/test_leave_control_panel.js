QUnit.module('hr');

QUnit.test("Test: Leave control panel [HR]", function (assert) {
	assert.expect(2);
	let done = assert.async();
	let today_date = finergy.datetime.nowdate();

	finergy.run_serially([
		// test leave allocation using leave control panel
		() => finergy.set_route("Form", "Leave Control Panel"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("leave_type", "Test Leave type"),
		() => cur_frm.set_value("company", "For Testing"),
		() => cur_frm.set_value("employment_type", "Test Employment Type"),
		() => cur_frm.set_value("branch", "Test Branch"),
		() => cur_frm.set_value("department", "Test Department"),
		() => cur_frm.set_value("designation", "Test Designation"),
		() => cur_frm.set_value("from_date", finergy.datetime.add_months(today_date, -2)),
		() => cur_frm.set_value("to_date", finergy.datetime.add_days(today_date, -1)),	// for two months [not today]
		() => cur_frm.set_value("no_of_days", 3),
		// allocate leaves
		() => finergy.click_button('Allocate'),
		() => finergy.timeout(1),
		() => assert.equal("Message", cur_dialog.title, "leave alloction message shown"),
		() => finergy.click_button('Close'),
		() => finergy.set_route("List", "Leave Allocation", "List"),
		() => finergy.timeout(1),
		() => {
			return finergy.call({
				method: "finergy.client.get_list",
				args: {
					doctype: "Employee",
					filters: {
						"branch": "Test Branch",
						"department": "Test Department",
						"company": "For Testing",
						"designation": "Test Designation",
						"status": "Active"
					}
				},
				callback: function(r) {
					let leave_allocated = cur_list.data.filter(d => d.leave_type == "Test Leave type");
					assert.equal(r.message.length, leave_allocated.length,
						'leave allocation successfully done for all the employees');
				}
			});
		},
		() => done()
	]);
});
