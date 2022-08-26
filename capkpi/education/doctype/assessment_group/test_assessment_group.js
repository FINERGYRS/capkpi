// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Group', function(assert){
	assert.expect(4);
	let done = assert.async();

	finergy.run_serially([
		() => finergy.set_route('Tree', 'Assessment Group'),

		// Checking adding child without selecting any Node
		() => finergy.tests.click_button('New'),
		() => finergy.timeout(0.2),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => finergy.tests.click_button('Close'),
		() => finergy.timeout(0.2),

		// Creating child nodes
		() => finergy.tests.click_link('All Assessment Groups'),
		() => finergy.map_group.make('Assessment-group-1'),
		() => finergy.map_group.make('Assessment-group-4', "All Assessment Groups", 1),
		() => finergy.tests.click_link('Assessment-group-4'),
		() => finergy.map_group.make('Assessment-group-5', "Assessment-group-3", 0),

		// Checking Edit button
		() => finergy.timeout(0.5),
		() => finergy.tests.click_link('Assessment-group-1'),
		() => finergy.tests.click_button('Edit'),
		() => finergy.timeout(0.5),
		() => {assert.deepEqual(finergy.get_route(), ["Form", "Assessment Group", "Assessment-group-1"], "Edit route checks");},

		// Deleting child Node
		() => finergy.set_route('Tree', 'Assessment Group'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_link('Assessment-group-1'),
		() => finergy.tests.click_button('Delete'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Yes'),

		// Checking Collapse and Expand button
		() => finergy.timeout(2),
		() => finergy.tests.click_link('Assessment-group-4'),
		() => finergy.click_button('Collapse'),
		() => finergy.tests.click_link('All Assessment Groups'),
		() => finergy.click_button('Collapse'),
		() => {assert.ok($('.opened').size() == 0, 'Collapsed');},
		() => finergy.click_button('Expand'),
		() => {assert.ok($('.opened').size() > 0, 'Expanded');},

		() => done()
	]);
});

finergy.map_group = {
	make:function(assessment_group_name, parent_assessment_group = 'All Assessment Groups', is_group = 0){
		return finergy.run_serially([
			() => finergy.click_button('Add Child'),
			() => finergy.timeout(0.2),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('assessment_group_name', assessment_group_name),
			() => cur_dialog.set_value('parent_assessment_group', parent_assessment_group),
			() => finergy.click_button('Create New'),
		]);
	}
};
