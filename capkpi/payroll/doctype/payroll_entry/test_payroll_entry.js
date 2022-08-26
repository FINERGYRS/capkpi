QUnit.module('HR');

QUnit.test("test: Payroll Entry", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let employees, docname;

	finergy.run_serially([
		() => {
			return finergy.tests.make('Payroll Entry', [
				{company: 'For Testing'},
				{posting_date: finergy.datetime.add_days(finergy.datetime.nowdate(), 0)},
				{payroll_frequency: 'Monthly'},
				{cost_center: 'Main - '+finergy.get_abbr(finergy.defaults.get_default("Company"))}
			]);
		},

		() => finergy.timeout(1),
		() => {
			assert.equal(cur_frm.doc.company, 'For Testing');
			assert.equal(cur_frm.doc.posting_date, finergy.datetime.add_days(finergy.datetime.nowdate(), 0));
			assert.equal(cur_frm.doc.cost_center, 'Main - FT');
		},
		() => finergy.click_button('Get Employee Details'),
		() => {
			employees = cur_frm.doc.employees.length;
			docname = cur_frm.doc.name;
		},

		() => finergy.click_button('Submit'),
		() => finergy.timeout(1),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(5),

		() => finergy.click_button('View Salary Slip'),
		() => finergy.timeout(2),
		() => assert.equal(cur_list.data.length, employees),

		() => finergy.set_route('Form', 'Payroll Entry', docname),
		() => finergy.timeout(2),
		() => finergy.click_button('Submit Salary Slip'),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(5),

		() => finergy.click_button('Close'),
		() => finergy.timeout(1),

		() => finergy.click_button('View Salary Slip'),
		() => finergy.timeout(2),
		() => {
			let count = 0;
			for(var i = 0; i < employees; i++) {
				if(cur_list.data[i].docstatus == 1){
					count++;
				}
			}
			assert.equal(count, employees, "Salary Slip submitted for all employees");
		},

		() => done()
	]);
});
