QUnit.module('accounts');

QUnit.test("test account", function(assert) {
	assert.expect(4);
	let done = assert.async();
	finergy.run_serially([
		() => finergy.set_route('Tree', 'Account'),
		() => finergy.timeout(3),
		() => finergy.click_button('Expand All'),
		() => finergy.timeout(1),
		() => finergy.click_link('Debtors'),
		() => finergy.click_button('Edit'),
		() => finergy.timeout(1),
		() => {
			assert.ok(cur_frm.doc.root_type=='Asset');
			assert.ok(cur_frm.doc.report_type=='Balance Sheet');
			assert.ok(cur_frm.doc.account_type=='Receivable');
		},
		() => finergy.click_button('Ledger'),
		() => finergy.timeout(1),
		() => {
			// check if general ledger report shown
			assert.deepEqual(finergy.get_route(), ['query-report', 'General Ledger']);
			window.history.back();
			return finergy.timeout(1);
		},
		() => done()
	]);
});
