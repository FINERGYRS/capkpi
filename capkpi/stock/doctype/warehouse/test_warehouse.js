QUnit.test("test: warehouse", function (assert) {
	assert.expect(0);
	let done = assert.async();

	finergy.run_serially([
		// test warehouse creation
		() => finergy.set_route("List", "Warehouse"),

		// Create a Laptop Scrap Warehouse
		() => finergy.tests.make(
			"Warehouse", [
				{warehouse_name: "Laptop Scrap Warehouse"},
				{company: "For Testing"}
			]
		),

		() => done()
	]);
});
