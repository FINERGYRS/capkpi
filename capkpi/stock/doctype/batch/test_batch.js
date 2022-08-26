QUnit.module('Stock');

QUnit.test("test Batch", function(assert) {
	assert.expect(1);
	let done = assert.async();
	finergy.run_serially([
		() => {
			return finergy.tests.make('Batch', [
				{batch_id:'TEST-BATCH-001'},
				{item:'Test Product 4'},
				{expiry_date:finergy.datetime.add_days(finergy.datetime.now_date(), 2)},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.batch_id=='TEST-BATCH-001', "Batch Id correct");
		},
		() => finergy.timeout(0.3),
		() => done()
	]);
});
