QUnit.module('hr');

QUnit.test("Test: Training Result [HR]", function (assert) {
	assert.expect(5);
	let done = assert.async();
	finergy.run_serially([
		// Creating Training Result
		() => finergy.set_route('List','Training Result','List'),
		() => finergy.timeout(0.3),
		() => finergy.click_button('Make a new Training Result'),
		() => {
			cur_frm.set_value('training_event','Test Training Event 1');
		},
		() => finergy.timeout(1),
		() => finergy.model.set_value('Training Result Employee','New Training Result Employee 1','hours',4),
		() => finergy.model.set_value('Training Result Employee','New Training Result Employee 1','grade','A'),
		() => finergy.model.set_value('Training Result Employee','New Training Result Employee 1','comments','Nice Seminar'),
		() => finergy.timeout(1),
		() => cur_frm.save(),
		() => finergy.timeout(1),
		() => cur_frm.save(),

		// Submitting the Training Result
		() => finergy.click_button('Submit'),
		() => finergy.click_button('Yes'),
		() => finergy.timeout(4),

		// Checking if the fields are correctly set
		() => {
			assert.equal('Test Training Event 1',cur_frm.get_field('training_event').value,
				'Training Result is created');

			assert.equal('Test Employee 1',cur_frm.doc.employees[0].employee_name,
				'Training Result is created for correct employee');

			assert.equal(4,cur_frm.doc.employees[0].hours,
				'Hours field is correctly calculated');

			assert.equal('A',cur_frm.doc.employees[0].grade,
				'Grade field is correctly set');
		},

		() => finergy.set_route('List','Training Result','List'),
		() => finergy.timeout(2),

		// Checking the submission of Training Result
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Training Result Submitted successfully');
		},
		() => done()
	]);
});
