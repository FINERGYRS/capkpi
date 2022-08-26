// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Result', function(assert){
	assert.expect(25);
	let done = assert.async();
	let student_list = [];
	let assessment_name;
	let tasks = []

	finergy.run_serially([
		// Saving Assessment Plan name
		() => finergy.db.get_value('Assessment Plan', {'assessment_name': 'Test-Mid-Term'}, 'name'),
		(assessment_plan) => {assessment_name = assessment_plan.message.name;},
		// Fetching list of Student for which Result is supposed to be set
		() => finergy.set_route('Form', 'Assessment Plan', assessment_name),
		() => finergy.timeout(1),
		() => finergy.tests.click_button('Assessment Result'),
		() => finergy.timeout(1),
		() => cur_frm.refresh(),
		() => finergy.timeout(1),
		() => {
			$("tbody tr").each( function(i, input){
				student_list.push($(input).data().student);
			});
		},

		// Looping through each student in the list and setting up their score
		() => {
			student_list.forEach(index => {
				tasks.push(
					() => finergy.set_route('List', 'Assessment Result', 'List'),
					() => finergy.timeout(0.5),
					() => finergy.tests.click_button('New'),
					() => finergy.timeout(0.5),
					() => cur_frm.set_value('student', index),
					() => cur_frm.set_value('assessment_plan', assessment_name),
					() => finergy.timeout(0.2),
					() => cur_frm.doc.details[0].score = (39 + (15 * student_list.indexOf(index))),
					() => cur_frm.save(),
					() => finergy.timeout(0.5),

					() => finergy.db.get_value('Assessment Plan', {'name': 'ASP00001'}, ['grading_scale', 'maximum_assessment_score']),
					(assessment_plan) => {
						assert.equal(cur_frm.doc.grading_scale, assessment_plan.message.grading_scale, 'Grading scale correctly fetched');
						assert.equal(cur_frm.doc.maximum_score, assessment_plan.message.maximum_assessment_score, 'Maximum score correctly fetched');

						finergy.call({
							method: "capkpi.education.api.get_grade",
							args: {
								"grading_scale": assessment_plan.message.grading_scale,
								"percentage": cur_frm.doc.total_score
							},
							callback: function(r){
								assert.equal(cur_frm.doc.grade, r.message, "Grade correctly calculated");
							}
						});
					},

					() => finergy.tests.click_button('Submit'),
					() => finergy.timeout(0.5),
					() => finergy.tests.click_button('Yes'),
					() => finergy.timeout(0.5),
					() => {assert.equal();},
					() => {assert.equal(cur_frm.doc.docstatus, 1, "Submitted successfully");},
				);
			});
			return finergy.run_serially(tasks);
		},

		() => done()
	]);
});
