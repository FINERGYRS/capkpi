// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Weather', {
	onload: (frm) => {
		if (frm.doc.weather_parameter == undefined) frm.call('load_contents');
	}
});
