QUnit.module('hr');

QUnit.test("Test: Leave application [HR]", function (assert) {
	assert.expect(4);
	let done = assert.async();
	let today_date = finergy.datetime.nowdate();
	let leave_date = finergy.datetime.add_days(today_date, 1);	// leave for tomorrow

	finergy.run_serially([
		// test creating leave application
		() => finergy.db.get_value('Employee', {'employee_name':'Test Employee 1'}, 'name'),
		(employee) => {
			return finergy.tests.make('Leave Application', [
				{leave_type: "Test Leave type"},
				{from_date: leave_date},	// for today
				{to_date: leave_date},
				{half_day: 1},
				{employee: employee.message.name},
				{follow_via_email: 0}
			]);
		},

		() => finergy.timeout(1),
		() => finergy.click_button('Actions'),
		() => finergy.click_link('Approve'), // approve the application [as administrator]
		() => finergy.click_button('Yes'),
		() => finergy.timeout(1),
		() => assert.ok(cur_frm.doc.docstatus,
			"leave application submitted after approval"),

		// check auto filled posting date [today]

		() => assert.equal(today_date, cur_frm.doc.posting_date,
			"posting date correctly set"),
		() => finergy.set_route("List", "Leave Application", "List"),
		() => finergy.timeout(1),
		// // check approved application in list
		() => assert.deepEqual(["Test Employee 1", 1], [cur_list.data[0].employee_name, cur_list.data[0].docstatus]),
		// 	"leave for correct employee is submitted"),
		() => done()
	]);
});
