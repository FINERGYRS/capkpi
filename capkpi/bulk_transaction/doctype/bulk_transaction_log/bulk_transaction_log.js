// Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Bulk Transaction Log', {

	refresh: function(frm) {
		frm.disable_save();
		frm.add_custom_button(__('Retry Failed Transactions'), ()=>{
			finergy.confirm(__("Retry Failing Transactions ?"), ()=>{
				query(frm, 1);
			}
			);
		});
	}
});

function query(frm) {
	finergy.call({
		method: "capkpi.bulk_transaction.doctype.bulk_transaction_log.bulk_transaction_log.retry_failing_transaction",
		args: {
			log_date: frm.doc.log_date
		}
	}).then((r) => {
		if (r.message === "No Failed Records") {
			finergy.show_alert(__(r.message), 5);
		} else {
			finergy.show_alert(__("Retrying Failed Transactions"), 5);
		}
	});
}