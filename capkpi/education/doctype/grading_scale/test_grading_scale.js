// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Grading Scale', function(assert){
	assert.expect(3);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Grading Scale', [
				{grading_scale_name: 'GTU'},
				{description: 'The score will be set according to 100 based system.'},
				{intervals: [
					[
						{grade_code: 'AA'},
						{threshold: '95'},
						{grade_description: 'First Class + Distinction'}
					],
					[
						{grade_code: 'AB'},
						{threshold: '90'},
						{grade_description: 'First Class'}
					],
					[
						{grade_code: 'BB'},
						{threshold: '80'},
						{grade_description: 'Distinction'}
					],
					[
						{grade_code: 'BC'},
						{threshold: '70'},
						{grade_description: 'Second Class'}
					],
					[
						{grade_code: 'CC'},
						{threshold: '60'},
						{grade_description: 'Third Class'}
					],
					[
						{grade_code: 'CD'},
						{threshold: '50'},
						{grade_description: 'Average'}
					],
					[
						{grade_code: 'DD'},
						{threshold: '40'},
						{grade_description: 'Pass'}
					],
					[
						{grade_code: 'FF'},
						{threshold: '0'},
						{grade_description: 'Fail'}
					],
				]}
			]);
		},
		() => {
			return finergy.tests.make('Grading Scale', [
				{grading_scale_name: 'GTU-2'},
				{description: 'The score will be set according to 100 based system.'},
				{intervals: [
					[
						{grade_code: 'AA'},
						{threshold: '90'},
						{grade_description: 'Distinction'}
					],
					[
						{grade_code: 'FF'},
						{threshold: '0'},
						{grade_description: 'Fail'}
					]
				]}
			]);
		},

		() => {
			let grading_scale = ['GTU', 'GTU-2'];
			let tasks = [];
			grading_scale.forEach(index => {
				tasks.push(
					() => finergy.set_route('Form', 'Grading Scale', index),
					() => finergy.timeout(0.5),
					() => finergy.tests.click_button('Submit'),
					() => finergy.timeout(0.5),
					() => finergy.tests.click_button('Yes'),
					() => {assert.equal(cur_frm.doc.docstatus, 1, 'Submitted successfully');}
				);
			});
			return finergy.run_serially(tasks);
		},

		() => finergy.timeout(1),
		() => finergy.set_route('Form', 'Grading Scale','GTU-2'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Cancel'),
		() => finergy.timeout(0.5),
		() => finergy.tests.click_button('Yes'),
		() => finergy.timeout(0.5),
		() => {assert.equal(cur_frm.doc.docstatus, 2, 'Cancelled successfully');},

		() => done()
	]);
});
