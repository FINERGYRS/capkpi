// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Criteria', function(assert){
	assert.expect(0);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Assessment Criteria', [
				{assessment_criteria: 'Pass'},
				{assessment_criteria_group: 'Reservation'}
			]);
		},
		() => done()
	]);
});
