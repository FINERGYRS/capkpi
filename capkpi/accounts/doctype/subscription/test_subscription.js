/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Subscription", function (assert) {
	assert.expect(4);
	let done = assert.async();
	finergy.run_serially([
		// insert a new Subscription
		() => {
			return finergy.tests.make("Subscription", [
				{reference_doctype: 'Sales Invoice'},
				{reference_document: 'SINV-00004'},
				{start_date: finergy.datetime.month_start()},
				{end_date: finergy.datetime.month_end()},
				{frequency: 'Weekly'}
			]);
		},
		() => cur_frm.savesubmit(),
		() => finergy.timeout(1),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(2),
		() => {
			assert.ok(cur_frm.doc.frequency.includes("Weekly"), "Set frequency Weekly");
			assert.ok(cur_frm.doc.reference_doctype.includes("Sales Invoice"), "Set base doctype Sales Invoice");
			assert.equal(cur_frm.doc.docstatus, 1, "Submitted subscription");
			assert.equal(cur_frm.doc.next_schedule_date,
				finergy.datetime.add_days(finergy.datetime.get_today(), 7),  "Set schedule date");
		},
		() => done()
	]);
});
