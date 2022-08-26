QUnit.module('accounts');

QUnit.test("test account with number", function(assert) {
	assert.expect(7);
	let done = assert.async();
	finergy.run_serially([
		() => finergy.set_route('Tree', 'Account'),
		() => finergy.click_link('Income'),
		() => finergy.click_button('Add Child'),
		() => finergy.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_name.$input.val("Test Income");
			cur_dialog.fields_dict.account_number.$input.val("4010");
		},
		() => finergy.click_button('Create New'),
		() => finergy.timeout(1),
		() => {
			assert.ok($('a:contains("4010 - Test Income"):visible').length!=0, "Account created with number");
		},
		() => finergy.click_link('4010 - Test Income'),
		() => finergy.click_button('Edit'),
		() => finergy.timeout(.5),
		() => finergy.click_button('Update Account Number'),
		() => finergy.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_number.$input.val("4020");
		},
		() => finergy.timeout(1),
		() => cur_dialog.primary_action(),
		() => finergy.timeout(1),
		() => cur_frm.refresh_fields(),
		() => finergy.timeout(.5),
		() => {
			var abbr = finergy.get_abbr(finergy.defaults.get_default("Company"));
			var new_account = "4020 - Test Income - " + abbr;
			assert.ok(cur_frm.doc.name==new_account, "Account renamed");
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4020", "Account number updated to 4020");
		},
		() => finergy.timeout(1),
		() => finergy.click_button('Menu'),
		() => finergy.click_link('Rename'),
		() => finergy.timeout(.5),
		() => {
			cur_dialog.fields_dict.new_name.$input.val("4030 - Test Income");
		},
		() => finergy.timeout(.5),
		() => finergy.click_button("Rename"),
		() => finergy.timeout(2),
		() => {
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4030", "Account number updated to 4030");
		},
		() => finergy.timeout(.5),
		() => finergy.click_button('Chart of Accounts'),
		() => finergy.timeout(.5),
		() => finergy.click_button('Menu'),
		() => finergy.click_link('Refresh'),
		() => finergy.click_button('Expand All'),
		() => finergy.click_link('4030 - Test Income'),
		() => finergy.click_button('Delete'),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(.5),
		() => {
			assert.ok($('a:contains("4030 - Test Account"):visible').length==0, "Account deleted");
		},
		() => done()
	]);
});
