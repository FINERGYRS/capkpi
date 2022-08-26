QUnit.module('HR');

QUnit.test("test: Set Salary Components", function (assert) {
	assert.expect(5);
	let done = assert.async();

	finergy.run_serially([
		() => finergy.set_route('Form', 'Salary Component', 'Leave Encashment'),
		() => {
			var row = finergy.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].account, 'Salary - FT'),

		() => finergy.set_route('Form', 'Salary Component', 'Basic'),
		() => {
			var row = finergy.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].account, 'Salary - FT'),

		() => finergy.set_route('Form', 'Salary Component', 'Income Tax'),
		() => {
			var row = finergy.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].account, 'Salary - FT'),

		() => finergy.set_route('Form', 'Salary Component', 'Arrear'),
		() => {
			var row = finergy.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].account, 'Salary - FT'),

		() => finergy.set_route('Form', 'Company', 'For Testing'),
		() => cur_frm.set_value('default_payroll_payable_account', 'Payroll Payable - FT'),
		() => cur_frm.save(),
		() => finergy.timeout(2),
		() => assert.equal(cur_frm.doc.default_payroll_payable_account, 'Payroll Payable - FT'),

		() => done()

	]);
});
