QUnit.test("test salary slip", function(assert) {
	assert.expect(6);
	let done = assert.async();
	let employee_name;

	let salary_slip = (ename) => {
		finergy.run_serially([
			() => finergy.db.get_value('Employee', {'employee_name': ename}, 'name'),
			(r) => {
				employee_name = r.message.name;
			},
			() => {
				// Creating a salary slip for a employee
				finergy.tests.make('Salary Slip', [
					{ employee: employee_name}
				]);
			},
			() => finergy.timeout(3),
			() => {
			// To check if all the calculations are correctly done
				if(ename === 'Test Employee 1')
				{
					assert.ok(cur_frm.doc.gross_pay==24000,
						'Gross amount for first employee is correctly calculated');
					assert.ok(cur_frm.doc.total_deduction==4800,
						'Deduction amount for first employee is correctly calculated');
					assert.ok(cur_frm.doc.net_pay==19200,
						'Net amount for first employee is correctly calculated');
				}
				if(ename === 'Test Employee 3')
				{
					assert.ok(cur_frm.doc.gross_pay==28800,
						'Gross amount for second employee is correctly calculated');
					assert.ok(cur_frm.doc.total_deduction==5760,
						'Deduction amount for second employee is correctly calculated');
					assert.ok(cur_frm.doc.net_pay==23040,
						'Net amount for second employee is correctly calculated');
				}
			},
		]);
	};
	finergy.run_serially([
		() => salary_slip('Test Employee 1'),
		() => finergy.timeout(6),
		() => salary_slip('Test Employee 3'),
		() => finergy.timeout(5),
		() => finergy.set_route('List', 'Salary Slip', 'List'),
		() => finergy.timeout(2),
		() => {$('.list-row-checkbox').click();},
		() => finergy.timeout(2),
		() => finergy.click_button('Delete'),
		() => finergy.click_button('Yes'),
		() => done()
	]);
});
