finergy.pages['team-updates'].on_page_load = function(wrapper) {
	var page = finergy.ui.make_app_page({
		parent: wrapper,
		title: __('Team Updates'),
		single_column: true
	});

	finergy.team_updates.make(page);
	finergy.team_updates.run();

	if(finergy.model.can_read('Daily Work Summary Group')) {
		page.add_menu_item(__('Daily Work Summary Group'), function() {
			finergy.set_route('Form', 'Daily Work Summary Group');
		});
	}
}

finergy.team_updates = {
	start: 0,
	make: function(page) {
		var me = finergy.team_updates;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			});
	},
	run: function() {
		var me = finergy.team_updates;
		finergy.call({
			method: 'capkpi.hr.page.team_updates.team_updates.get_data',
			args: {
				start: me.start
			},
			callback: function(r) {
				if (r.message && r.message.length > 0) {
					r.message.forEach(function(d) {
						me.add_row(d);
					});
				} else {
					finergy.show_alert({message: __('No more updates'), indicator: 'gray'});
					me.more.parent().addClass('hidden');
				}
			}
		});
	},
	add_row: function(data) {
		var me = finergy.team_updates;

		data.by = finergy.user.full_name(data.sender);
		data.avatar = finergy.avatar(data.sender);
		data.when = comment_when(data.creation);

		var date = finergy.datetime.str_to_obj(data.creation);
		var last = me.last_feed_date;

		if((last && finergy.datetime.obj_to_str(last) != finergy.datetime.obj_to_str(date)) || (!last)) {
			var diff = finergy.datetime.get_day_diff(finergy.datetime.get_today(), finergy.datetime.obj_to_str(date));
			var pdate;
			if(diff < 1) {
				pdate = 'Today';
			} else if(diff < 2) {
				pdate = 'Yesterday';
			} else {
				pdate = finergy.datetime.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate=='Today' ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		me.last_feed_date = date;

		$(finergy.render_template('team_update_row', data)).appendTo(me.body);
	}
}
