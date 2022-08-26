// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Topic', {
	refresh: function(frm) {
		if (!cur_frm.doc.__islocal) {
			frm.add_custom_button(__('Add to Courses'), function() {
				frm.trigger('add_topic_to_courses');
			}, __('Action'));
		}
	},

	add_topic_to_courses: function(frm) {
		get_courses_without_topic(frm.doc.name).then(r => {
			if (r.message.length) {
				finergy.prompt([
					{
						fieldname: 'courses',
						label: __('Courses'),
						fieldtype: 'MultiSelectPills',
						get_data: function() {
							return r.message;
						}
					}
				],
				function(data) {
					finergy.call({
						method: 'capkpi.education.doctype.topic.topic.add_topic_to_courses',
						args: {
							'topic': frm.doc.name,
							'courses': data.courses
						},
						callback: function(r) {
							if (!r.exc) {
								frm.reload_doc();
							}
						},
						freeze: true,
						freeze_message: __('...Adding Topic to Courses')
					});
				}, __('Add Topic to Courses'), __('Add'));
			} else {
				finergy.msgprint(__('This topic is already added to the existing courses'));
			}
		});
	}
});

let get_courses_without_topic = function(topic) {
	return finergy.call({
		type: 'GET',
		method: 'capkpi.education.doctype.topic.topic.get_courses_without_topic',
		args: {'topic': topic}
	});
};
