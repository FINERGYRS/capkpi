QUnit.test("Test: Company", function (assert) {
	assert.expect(0);

	let done = assert.async();

	finergy.run_serially([
		// Added company for Work Order testing
		() => finergy.set_route("List", "Company"),
		() => finergy.new_doc("Company"),
		() => finergy.timeout(1),
		() => cur_frm.set_value("company_name", "For Testing"),
		() => cur_frm.set_value("abbr", "RB"),
		() => cur_frm.set_value("default_currency", "INR"),
		() => cur_frm.save(),
		() => finergy.timeout(1),

		() => done()
	]);
});