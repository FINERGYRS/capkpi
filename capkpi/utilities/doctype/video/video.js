// Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Video', {
	refresh: function (frm) {
		frm.events.toggle_youtube_statistics_section(frm);
		frm.add_custom_button("Watch Video", () => finergy.help.show_video(frm.doc.url, frm.doc.title));
	},

	toggle_youtube_statistics_section: (frm) => {
		if (frm.doc.provider === "YouTube") {
			finergy.db.get_single_value("Video Settings", "enable_youtube_tracking").then( val => {
				frm.toggle_display("youtube_tracking_section", val);
			});
		}
	}
});
