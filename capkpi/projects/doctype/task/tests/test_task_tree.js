/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Task Tree", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(4);

	finergy.run_serially([
		// insert a new Task
		() => finergy.set_route('Tree', 'Task'),
		() => finergy.timeout(0.5),

		// Checking adding child without selecting any Node
		() => finergy.tests.click_button('New'),
		() => finergy.timeout(0.5),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => finergy.tests.click_button('Close'),
		() => finergy.timeout(0.5),

		// Creating child nodes
		() => finergy.tests.click_link('All Tasks'),
		() => finergy.map_group.make('Test-1'),
		() => finergy.map_group.make('Test-3', 1),
		() => finergy.timeout(1),
		() => finergy.tests.click_link('Test-3'),
		() => finergy.map_group.make('Test-4', 0),

		// Checking Edit button
		() => finergy.timeout(0.5),
		() => finergy.tests.click_link('Test-1'),
		() => finergy.tests.click_button('Edit'),
		() => finergy.timeout(1),
		() => finergy.db.get_value('Task', {'subject': 'Test-1'}, 'name'),
		(task) => {assert.deepEqual(finergy.get_route(), ["Form", "Task", task.message.name], "Edit route checks");},

		// Deleting child Node
		() => finergy.set_route('Tree', 'Task'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_link('Test-1'),
		() => finergy.tests.click_button('Delete'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Yes'),

		// Deleting Group Node that has child nodes in it
		() => finergy.timeout(0.5),
		() => finergy.tests.click_link('Test-3'),
		() => finergy.tests.click_button('Delete'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(1),
		() => {assert.equal(cur_dialog.title, 'Message', 'Error thrown correctly');},
		() => finergy.tests.click_button('Close'),

		// Add multiple child tasks
		() => finergy.tests.click_link('Test-3'),
		() => finergy.timeout(0.5),
		() => finergy.click_button('Add Multiple'),
		() => finergy.timeout(1),
		() => cur_dialog.set_value('tasks', 'Test-6\nTest-7'),
		() => finergy.timeout(0.5),
		() => finergy.click_button('Submit'),
		() => finergy.timeout(2),
		() => finergy.click_button('Expand All'),
		() => finergy.timeout(1),
		() => {
			let count = $(`a:contains("Test-6"):visible`).length + $(`a:contains("Test-7"):visible`).length;
			assert.equal(count, 2, "Multiple Tasks added successfully");
		},

		() => done()
	]);
});

finergy.map_group = {
	make:function(subject, is_group = 0){
		return finergy.run_serially([
			() => finergy.click_button('Add Child'),
			() => finergy.timeout(1),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('subject', subject),
			() => finergy.click_button('Create New'),
			() => finergy.timeout(1.5)
		]);
	}
};
