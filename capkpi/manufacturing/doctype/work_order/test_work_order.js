QUnit.test("test: work order", function (assert) {
	assert.expect(25);
	let done = assert.async();
	let laptop_quantity = 5;
	let items = ["CPU", "Keyboard", "Screen"];
	let operation_items = ["CPU", "Keyboard", "Screen"];
	let click_make = () => {
		let element = $(`.btn-primary:contains("Make"):visible`);
		if(!element.length) {
			throw `did not find any button containing 'Make'`;
		}
		element.click();
		return finergy.timeout(1);
	};

	finergy.run_serially([
		// test work order
		() => finergy.set_route("List", "Work Order", "List"),
		() => finergy.timeout(3),

		// Create a laptop work order
		() => {
			return finergy.tests.make('Work Order', [
				{production_item: 'Laptop'},
				{company: 'For Testing'},
				{qty: laptop_quantity},
				{scrap_warehouse: "Laptop Scrap Warehouse - FT"},
				{wip_warehouse: "Work In Progress - FT"},
				{fg_warehouse: "Finished Goods - FT"}
			]);
		},
		() => finergy.timeout(3),
		() => {
			assert.equal(cur_frm.doc.planned_operating_cost, cur_frm.doc.total_operating_cost,
				"Total and Planned Cost is equal");
			assert.equal(cur_frm.doc.planned_operating_cost, cur_frm.doc.total_operating_cost,
				"Total and Planned Cost is equal");

			items.forEach(function(item, index) {
				assert.equal(item, cur_frm.doc.required_items[index].item_code, `Required item ${item} added`);
				assert.equal("Stores - FT", cur_frm.doc.required_items[index].source_warehouse, `Item ${item} warhouse verified`);
				assert.equal("5", cur_frm.doc.required_items[index].required_qty, `Item ${item} quantity verified`);
			});

			operation_items.forEach(function(operation_item, index) {
				assert.equal(`Assemble ${operation_item}`, cur_frm.doc.operations[index].operation,
					`Operation ${operation_item} added`);
				assert.equal(`${operation_item} assembly workstation`, cur_frm.doc.operations[index].workstation,
					`Workstation ${operation_item} linked`);
			});
		},

		// Submit the work order
		() => cur_frm.savesubmit(),
		() => finergy.timeout(1),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(2.5),

		// Confirm the work order timesheet, save and submit it
		() => finergy.click_link("TS-00"),
		() => finergy.timeout(1),
		() => finergy.click_button("Submit"),
		() => finergy.timeout(1),
		() => finergy.click_button("Yes"),
		() => finergy.timeout(2.5),

		// Start the work order process
		() => finergy.set_route("List", "Work Order", "List"),
		() => finergy.timeout(2),
		() => finergy.click_link("Laptop"),
		() => finergy.timeout(1),
		() => finergy.click_button("Start"),
		() => finergy.timeout(0.5),
		() => click_make(),
		() => finergy.timeout(1),
		() => finergy.click_button("Save"),
		() => finergy.timeout(0.5),

		() => {
			assert.equal(cur_frm.doc.total_outgoing_value, cur_frm.doc.total_incoming_value,
				"Total incoming and outgoing cost is equal");
			assert.equal(cur_frm.doc.total_outgoing_value, "99000",
				"Outgoing cost is correct"); // Price of each item x5
		},
		// Submit for work
		() => finergy.click_button("Submit"),
		() => finergy.timeout(0.5),
		() => finergy.click_button("Yes"),
		() => finergy.timeout(0.5),

		// Finish the work order by sending for manufacturing
		() => finergy.set_route("List", "Work Order"),
		() => finergy.timeout(1),
		() => finergy.click_link("Laptop"),
		() => finergy.timeout(1),

		() => {
			assert.ok(finergy.tests.is_visible("5 items in progress", 'p'), "Work order initiated");
			assert.ok(finergy.tests.is_visible("Finish"), "Finish button visible");
		},

		() => finergy.click_button("Finish"),
		() => finergy.timeout(0.5),
		() => click_make(),
		() => {
			assert.equal(cur_frm.doc.total_incoming_value, "105700",
				"Incoming cost is correct "+cur_frm.doc.total_incoming_value); // Price of each item x5, values are in INR
			assert.equal(cur_frm.doc.total_outgoing_value, "99000",
				"Outgoing cost is correct"); // Price of each item x5, values are in INR
			assert.equal(cur_frm.doc.total_incoming_value - cur_frm.doc.total_outgoing_value, cur_frm.doc.value_difference,
				"Value difference is correct"); // Price of each item x5, values are in INR
		},
		() => finergy.click_button("Save"),
		() => finergy.timeout(1),
		() => finergy.click_button("Submit"),
		() => finergy.timeout(1),
		() => finergy.click_button("Yes"),
		() => finergy.timeout(1),

		// Manufacturing finished
		() => finergy.set_route("List", "Work Order", "List"),
		() => finergy.timeout(1),
		() => finergy.click_link("Laptop"),
		() => finergy.timeout(1),

		() => assert.ok(finergy.tests.is_visible("5 items produced", 'p'), "Work order completed"),

		() => done()
	]);
});
