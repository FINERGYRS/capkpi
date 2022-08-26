QUnit.module('accounts');
QUnit.test("test account", assert => {
	assert.expect(3);
	let done = assert.async();
	finergy.run_serially([
		() => finergy.set_route('Tree', 'Account'),
		() => finergy.click_button('Expand All'),
		() => finergy.click_link('Duties and Taxes - '+ finergy.get_abbr(finergy.defaults.get_default("Company"))),
		() => {
			if($('a:contains("CGST"):visible').length == 0){
				return finergy.map_tax.make('CGST', 9);
			}
		},
		() => {
			if($('a:contains("SGST"):visible').length == 0){
				return finergy.map_tax.make('SGST', 9);
			}
		},
		() => {
			if($('a:contains("IGST"):visible').length == 0){
				return finergy.map_tax.make('IGST', 18);
			}
		},
		() => {
			assert.ok($('a:contains("CGST"):visible').length!=0, "CGST Checked");
			assert.ok($('a:contains("SGST"):visible').length!=0, "SGST Checked");
			assert.ok($('a:contains("IGST"):visible').length!=0, "IGST Checked");
		},
		() => done()
	]);
});


finergy.map_tax = {
	make:function(text,rate){
		return finergy.run_serially([
			() => finergy.click_button('Add Child'),
			() => finergy.timeout(0.2),
			() => cur_dialog.set_value('account_name',text),
			() => cur_dialog.set_value('account_type','Tax'),
			() => cur_dialog.set_value('tax_rate',rate),
			() => cur_dialog.set_value('account_currency','INR'),
			() => finergy.click_button('Create New'),
		]);
	}
};
