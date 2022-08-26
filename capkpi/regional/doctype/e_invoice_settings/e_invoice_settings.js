// Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('E Invoice Settings', {
	refresh(frm) {
		const docs_link = 'https://docs.capkpi.com/docs/v13/user/manual/en/regional/india/setup-e-invoicing';
		frm.dashboard.set_headline(
			__("Read {0} for more information on E Invoicing features.", [`<a href='${docs_link}'>documentation</a>`])
		);
	}
});
