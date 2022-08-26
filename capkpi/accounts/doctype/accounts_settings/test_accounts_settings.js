QUnit.module('accounts');

QUnit.test("test: Accounts Settings doesn't allow negatives", function (assert) {
	let done = assert.async();

	assert.expect(2);

	finergy.run_serially([
		() => finergy.set_route('Form', 'Accounts Settings', 'Accounts Settings'),
		() => finergy.timeout(2),
		() => unchecked_if_checked(cur_frm, 'Allow Stale Exchange Rates', finergy.click_check),
		() => cur_frm.set_value('stale_days', 0),
		() => finergy.click_button('Save'),
		() => finergy.timeout(2),
		() => {
			assert.ok(cur_dialog);
		},
		() => finergy.click_button('Close'),
		() => cur_frm.set_value('stale_days', -1),
		() => finergy.click_button('Save'),
		() => finergy.timeout(2),
		() => {
			assert.ok(cur_dialog);
		},
		() => finergy.click_button('Close'),
		() => done()
	]);

});

const unchecked_if_checked = function(frm, field_name, fn){
	if (frm.doc.allow_stale) {
		return fn(field_name);
	}
};
