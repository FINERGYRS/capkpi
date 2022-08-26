// Testing Attendance Module in Education
QUnit.module('education');

QUnit.test('Test: Student Leave Application', function(assert){
	assert.expect(4);
	let done = assert.async();
	let student_code;
	let leave_code;
	finergy.run_serially([
		() => finergy.db.get_value('Student', {'student_email_id': 'test2@testmail.com'}, 'name'),
		(student) => {student_code = student.message.name;}, // fetching student code from db

		() => {
			return finergy.tests.make('Student Leave Application', [
				{student: student_code},
				{from_date: '2017-08-02'},
				{to_date: '2017-08-04'},
				{mark_as_present: 0},
				{reason: "Sick Leave."}
			]);
		},
		() => finergy.tests.click_button('Submit'), // Submitting the leave application
		() => finergy.timeout(0.7),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.7),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1, "Submitted leave application");
			leave_code = finergy.get_route()[2];
		},
		() => finergy.tests.click_button('Cancel'), // Cancelling the leave application
		() => finergy.timeout(0.7),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(1),
		() => {assert.equal(cur_frm.doc.docstatus, 2, "Cancelled leave application");},
		() => finergy.tests.click_button('Amend'), // Amending the leave application
		() => finergy.timeout(1),
		() => {
			cur_frm.doc.mark_as_present = 1;
			cur_frm.save();
		},
		() => finergy.timeout(0.7),
		() => finergy.tests.click_button('Submit'),
		() => finergy.timeout(0.7),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.7),
		() => {assert.equal(cur_frm.doc.amended_from, leave_code, "Amended successfully");},

		() => finergy.timeout(0.5),
		() => {
			return finergy.tests.make('Student Leave Application', [
				{student: student_code},
				{from_date: '2017-08-07'},
				{to_date: '2017-08-09'},
				{mark_as_present: 0},
				{reason: "Sick Leave."}
			]);
		},
		() => finergy.tests.click_button('Submit'),
		() => finergy.timeout(0.7),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.7),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1, "Submitted leave application");
			leave_code = finergy.get_route()[2];
		},

		() => done()
	]);
});
