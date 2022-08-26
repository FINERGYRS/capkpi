capkpi.ItemSelector = Class.extend({
	init: function(opts) {
		$.extend(this, opts);

		if (!this.item_field) {
			this.item_field = 'item_code';
		}

		if (!this.item_query) {
			this.item_query = capkpi.queries.item().query;
		}

		this.grid = this.frm.get_field("items").grid;
		this.setup();
	},

	setup: function() {
		var me = this;
		if(!this.grid.add_items_button) {
			this.grid.add_items_button = this.grid.add_custom_button(__('Add Items'), function() {
				if(!me.dialog) {
					me.make_dialog();
				}
				me.dialog.show();
				me.render_items();
				setTimeout(function() { me.dialog.input.focus(); }, 1000);
			});
		}
	},

	make_dialog: function() {
		this.dialog = new finergy.ui.Dialog({
			title: __('Add Items')
		});
		var body = $(this.dialog.body);
		body.html('<div><p><input type="text" class="form-control"></p>\
			<br><div class="results"></div></div>');

		this.dialog.input = body.find('.form-control');
		this.dialog.results = body.find('.results');

		var me = this;
		this.dialog.results.on('click', '.image-view-item', function() {
			me.add_item($(this).attr('data-name'));
		});

		this.dialog.input.on('keyup', function() {
			if(me.timeout_id) {
				clearTimeout(me.timeout_id);
			}
			me.timeout_id = setTimeout(function() {
				me.render_items();
				me.timeout_id = undefined;
			}, 500);
		});
	},

	add_item: function(item_code) {
		// add row or update qty
		var added = false;

		// find row with item if exists
		$.each(this.frm.doc.items || [], (i, d) => {
			if(d[this.item_field]===item_code) {
				finergy.model.set_value(d.doctype, d.name, 'qty', d.qty + 1);
				finergy.show_alert({message: __("Added {0} ({1})", [item_code, d.qty]), indicator: 'green'});
				added = true;
				return false;
			}
		});

		if(!added) {
			var d = null;
			finergy.run_serially([
				() => { d = this.grid.add_new_row(); },
				() => finergy.model.set_value(d.doctype, d.name, this.item_field, item_code),
				() => finergy.timeout(0.1),
				() => {
					finergy.model.set_value(d.doctype, d.name, 'qty', 1);
					finergy.show_alert({message: __("Added {0} ({1})", [item_code, 1]), indicator: 'green'});
				}
			]);
		}

	},

	render_items: function() {
		let args = {
			query: this.item_query,
			filters: {}
		};
		args.txt = this.dialog.input.val();
		args.as_dict = 1;

		if (this.get_filters) {
			$.extend(args.filters, this.get_filters() || {});
		}

		var me = this;
		finergy.link_search("Item", args, function(r) {
			$.each(r.values, function(i, d) {
				if(!d.image) {
					d.abbr = finergy.get_abbr(d.item_name);
					d.color = finergy.get_palette(d.item_name);
				}
			});
			me.dialog.results.html(finergy.render_template('item_selector', {'data':r.values}));
		});
	}
});
