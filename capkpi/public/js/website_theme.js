// Copyright (c) 2019, Finergy Reporting Solutions SAS and Contributors
// MIT License. See license.txt

finergy.ui.form.on('Website Theme', {
	validate(frm) {
		let theme_scss = frm.doc.theme_scss;
		if (theme_scss && theme_scss.includes('finergy/public/scss/website')
			&& !theme_scss.includes('capkpi/public/scss/website')
		) {
			frm.set_value('theme_scss',
				`${frm.doc.theme_scss}\n@import "capkpi/public/scss/website";`);
		}
	}
});
