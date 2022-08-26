QUnit.module('education');

QUnit.test('Test: Student Group Creation Tool', function(assert){
	assert.expect(5);
	let done = assert.async();
	let instructor_code;

	finergy.run_serially([
		// Saving Instructor code beforehand
		() => finergy.db.get_value('Instructor', {'instructor_name': 'Instructor 1'}, 'name'),
		(instructor) => {instructor_code = instructor.message.name;},

		// Setting up the creation tool to generate and save Student Group
		() => finergy.set_route('Form', 'Student Group Creation Tool'),
		() => finergy.timeout(0.5),
		() => {
			cur_frm.set_value("academic_year", "2016-17");
			cur_frm.set_value("academic_term", "2016-17 (Semester 1)");
			cur_frm.set_value("program", "Standard Test");
			finergy.tests.click_button('Get Courses');
		},
		() => finergy.timeout(1),
		() => {
			let no_of_courses = $('input.grid-row-check.pull-left').size() - 1;
			assert.equal(cur_frm.doc.courses.length, no_of_courses, 'Successfully created groups using the tool');
		},

		() => {
			let d, grid, grid_row;

			for(d = 0; d < cur_frm.doc.courses.length; d++)
			{
				grid = cur_frm.get_field("courses").grid;
				grid_row = grid.get_row(d).toggle_view(true);
				if(grid_row.doc.student_group_name == 'Standard Test/A/2016-17 (Semester 1)'){
					grid_row.doc.max_strength = 10;
					grid_row.doc.student_group_name = "test-batch-wise-group-2";
					$(`.octicon.octicon-triangle-up`).click();
					continue;
				}
				else if(grid_row.doc.student_group_name == 'Test_Sub/Standard Test/2016-17 (Semester 1)'){
					grid_row.doc.max_strength = 10;
					grid_row.doc.student_group_name = "test-course-wise-group-2";
					$(`.octicon.octicon-triangle-up`).click();
					continue;
				}
			}
		},

		// Generating Student Group
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button("Create Student Groups"),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button("Close"),

		// Goin to the generated group to set up student and instructor list
		() => {
			let group_name = ['Student Group/test-batch-wise-group-2', 'Student Group/test-course-wise-group-2'];
			let tasks = [];
			group_name.forEach(index => {
				tasks.push(
					() => finergy.timeout(1),
					() => finergy.set_route("Form", index),
					() => finergy.timeout(0.5),
					() => {
						assert.equal(cur_frm.doc.students.length, 5, 'Successfully fetched list of students');
					},
					() => finergy.timeout(0.5),
					() => {
						d = cur_frm.add_child('instructors');
						d.instructor = instructor_code;
						cur_frm.save();
					},
					() => {
						assert.equal(cur_frm.doc.instructors.length, 1, 'Instructor detail stored successfully');
					},
				);
			});
			return finergy.run_serially(tasks);
		},

		() => done()
	]);
});
