// Testing Assessment Module in education
QUnit.module('education');

QUnit.test('Test: Assessment Plan', function(assert){
	assert.expect(6);
	let done = assert.async();
	let room_name, instructor_name, assessment_name;

	finergy.run_serially([
		() => finergy.db.get_value('Room', {'room_name': 'Room 1'}, 'name'),
		(room) => {room_name = room.message.name;}, // Fetching Room name
		() => finergy.db.get_value('Instructor', {'instructor_name': 'Instructor 1'}, 'name'),
		(instructor) => {instructor_name = instructor.message.name;}, // Fetching Instructor name

		() => {
			return finergy.tests.make('Assessment Plan', [
				{assessment_name: "Test-Mid-Term"},
				{assessment_group: 'Assessment-group-5'},
				{maximum_assessment_score: 100},
				{student_group: 'test-course-wise-group-2'},
				{course: 'Test_Sub'},
				{grading_scale: 'GTU'},
				{schedule_date: finergy.datetime.nowdate()},
				{room: room_name},
				{examiner: instructor_name},
				{supervisor: instructor_name},
				{from_time: "12:30:00"},
				{to_time: "2:30:00"}
			]);
		},

		() => {
			assessment_name = cur_frm.doc.name; // Storing the name of current Assessment Plan
			assert.equal(cur_frm.doc.assessment_criteria[0].assessment_criteria, 'Pass', 'Assessment Criteria auto-filled correctly');
			assert.equal(cur_frm.doc.assessment_criteria[0].maximum_score, 100, 'Maximum score correctly set');
		}, // Checking if the table was auto-filled upon selecting appropriate fields

		() => finergy.timeout(1),
		() => finergy.tests.click_button('Submit'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.5),
		() => {assert.equal(cur_frm.doc.docstatus, 1, "Assessment Plan submitted successfully");},

		() => finergy.click_button('Assessment Result'), // Checking out Assessment Result button option
		() => finergy.timeout(0.5),
		() => {
			assert.deepEqual(finergy.get_route(), ["Form", "Assessment Result Tool"], 'Assessment Result properly linked');
			assert.equal(cur_frm.doc.assessment_plan, assessment_name, 'Assessment correctly set');
			assert.equal(cur_frm.doc.student_group, 'test-course-wise-group-2', 'Course for Assessment correctly set');
		},
		() => done()
	]);
});
