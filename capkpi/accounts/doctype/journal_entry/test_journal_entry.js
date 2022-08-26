QUnit.module('Journal Entry');

QUnit.test("test journal entry", function(assert) {
	assert.expect(2);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Journal Entry', [
				{posting_date:finergy.datetime.add_days(finergy.datetime.nowdate(), 0)},
				{accounts: [
					[
						{'account':'Debtors - '+finergy.get_abbr(finergy.defaults.get_default('Company'))},
						{'party_type':'Customer'},
						{'party':'Test Customer 1'},
						{'credit_in_account_currency':1000},
						{'is_advance':'Yes'},
					],
					[
						{'account':'HDFC - '+finergy.get_abbr(finergy.defaults.get_default('Company'))},
						{'debit_in_account_currency':1000},
					]
				]},
				{cheque_no:1234},
				{cheque_date: finergy.datetime.add_days(finergy.datetime.nowdate(), -1)},
				{user_remark: 'Test'},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.total_debit==1000, "total debit correct");
			assert.ok(cur_frm.doc.total_credit==1000, "total credit correct");
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.3),
		() => done()
	]);
});
