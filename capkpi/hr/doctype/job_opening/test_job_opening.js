QUnit.module('hr');

QUnit.test("Test: Job Opening [HR]", function (assert) {
	assert.expect(2);
	let done = assert.async();

	finergy.run_serially([
		// Job Opening creation
		() => {
			finergy.tests.make('Job Opening', [
				{ job_title: 'Software Developer'},
				{ description:
					'You might be responsible for writing and coding individual'+
					' programmes or providing an entirely new software resource.'}
			]);
		},
		() => finergy.timeout(4),
		() => finergy.set_route('List','Job Opening'),
		() => finergy.timeout(3),
		() => {
			assert.ok(cur_list.data.length==1, 'Job Opening created successfully');
			assert.ok(cur_list.data[0].job_title=='Software Developer', 'Job title Correctly set');
		},
		() => done()
	]);
});
