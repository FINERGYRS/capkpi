// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Fertilizer', {
	onload: (frm) => {
		if (frm.doc.fertilizer_contents == undefined) frm.call('load_contents');
	}
});
