// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors // License: GNU General Public License v3. See license.txt

finergy.provide("capkpi.stock");
finergy.provide("capkpi.accounts.dimensions");

{% include 'capkpi/stock/landed_taxes_and_charges_common.js' %};

finergy.ui.form.on('Stock Entry', {
	setup: function(frm) {
		frm.set_indicator_formatter('item_code', function(doc) {
			if (!doc.s_warehouse) {
				return 'blue';
			} else {
				return (doc.qty<=doc.actual_qty) ? 'green' : 'orange';
			}
		});

		frm.set_query('work_order', function() {
			return {
				filters: [
					['Work Order', 'docstatus', '=', 1],
					['Work Order', 'qty', '>','`tabWork Order`.produced_qty'],
					['Work Order', 'company', '=', frm.doc.company]
				]
			}
		});

		frm.set_query('outgoing_stock_entry', function() {
			return {
				filters: [
					['Stock Entry', 'docstatus', '=', 1],
					['Stock Entry', 'per_transferred', '<','100'],
				]
			}
		});

		frm.set_query('source_warehouse_address', function() {
			return {
				filters: {
					link_doctype: 'Warehouse',
					link_name: frm.doc.from_warehouse
				}
			}
		});

		frm.set_query('target_warehouse_address', function() {
			return {
				filters: {
					link_doctype: 'Warehouse',
					link_name: frm.doc.to_warehouse
				}
			}
		});

		finergy.db.get_value('Stock Settings', {name: 'Stock Settings'}, 'sample_retention_warehouse', (r) => {
			if (r.sample_retention_warehouse) {
				var filters = [
							["Warehouse", 'company', '=', frm.doc.company],
							["Warehouse", "is_group", "=",0],
							['Warehouse', 'name', '!=', r.sample_retention_warehouse]
						]
				frm.set_query("from_warehouse", function() {
					return {
						filters: filters
					};
				});
				frm.set_query("s_warehouse", "items", function() {
					return {
						filters: filters
					};
				});
			}
		});

		frm.set_query('batch_no', 'items', function(doc, cdt, cdn) {
			var item = locals[cdt][cdn];
			if(!item.item_code) {
				finergy.throw(__("Please enter Item Code to get Batch Number"));
			} else {
				if (in_list(["Material Transfer for Manufacture", "Manufacture", "Repack", "Send to Subcontractor"], doc.purpose)) {
					var filters = {
						'item_code': item.item_code,
						'posting_date': frm.doc.posting_date || finergy.datetime.nowdate()
					}
				} else {
					var filters = {
						'item_code': item.item_code
					}
				}

				// User could want to select a manually created empty batch (no warehouse)
				// or a pre-existing batch
				if (frm.doc.purpose != "Material Receipt") {
					filters["warehouse"] = item.s_warehouse || item.t_warehouse;
				}

				return {
					query : "capkpi.controllers.queries.get_batch_no",
					filters: filters
				}
			}
		});


		frm.add_fetch("bom_no", "inspection_required", "inspection_required");
		capkpi.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);

		finergy.db.get_single_value('Stock Settings', 'disable_serial_no_and_batch_selector')
		.then((value) => {
			if (value) {
				finergy.flags.hide_serial_batch_dialog = true;
			}
		});
		attach_bom_items(frm.doc.bom_no);
	},

	setup_quality_inspection: function(frm) {
		if (!frm.doc.inspection_required) {
			return;
		}

		if (!frm.is_new() && frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Quality Inspection(s)"), () => {
				let transaction_controller = new capkpi.TransactionController({ frm: frm });
				transaction_controller.make_quality_inspection();
			}, __("Create"));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		let quality_inspection_field = frm.get_docfield("items", "quality_inspection");
		quality_inspection_field.get_route_options_for_new_doc = function(row) {
			if (frm.is_new()) return;
			return {
				"inspection_type": "Incoming",
				"reference_type": frm.doc.doctype,
				"reference_name": frm.doc.name,
				"item_code": row.doc.item_code,
				"description": row.doc.description,
				"item_serial_no": row.doc.serial_no ? row.doc.serial_no.split("\n")[0] : null,
				"batch_no": row.doc.batch_no
			}
		}

		frm.set_query("quality_inspection", "items", function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];

			return {
				query:"capkpi.stock.doctype.quality_inspection.quality_inspection.quality_inspection_query",
				filters: {
					'item_code': d.item_code,
					'reference_name': doc.name
				}
			}
		});
	},

	outgoing_stock_entry: function(frm) {
		finergy.call({
			doc: frm.doc,
			method: "set_items_for_stock_in",
			callback: function() {
				refresh_field('items');
			}
		});
	},

	refresh: function(frm) {
		if(!frm.doc.docstatus) {
			frm.trigger('validate_purpose_consumption');
			frm.add_custom_button(__('Material Request'), function() {
				finergy.model.with_doctype('Material Request', function() {
					var mr = finergy.model.get_new_doc('Material Request');
					var items = frm.get_field('items').grid.get_selected_children();
					if(!items.length) {
						items = frm.doc.items;
					}
					items.forEach(function(item) {
						var mr_item = finergy.model.add_child(mr, 'items');
						mr_item.item_code = item.item_code;
						mr_item.item_name = item.item_name;
						mr_item.uom = item.uom;
						mr_item.stock_uom = item.stock_uom;
						mr_item.conversion_factor = item.conversion_factor;
						mr_item.item_group = item.item_group;
						mr_item.description = item.description;
						mr_item.image = item.image;
						mr_item.qty = item.qty;
						mr_item.warehouse = item.s_warehouse;
						mr_item.required_date = finergy.datetime.nowdate();
					});
					finergy.set_route('Form', 'Material Request', mr.name);
				});
			}, __("Create"));
		}

		if(frm.doc.items) {
			const has_alternative = frm.doc.items.find(i => i.allow_alternative_item === 1);

			if (frm.doc.docstatus == 0 && has_alternative) {
				frm.add_custom_button(__('Alternate Item'), () => {
					capkpi.utils.select_alternate_items({
						frm: frm,
						child_docname: "items",
						warehouse_field: "s_warehouse",
						child_doctype: "Stock Entry Detail",
						original_item_field: "original_item",
						condition: (d) => {
							if (d.s_warehouse && d.allow_alternative_item) {return true;}
						}
					})
				});
			}
		}

		if (frm.doc.docstatus === 1) {
			if (frm.doc.add_to_transit && frm.doc.purpose=='Material Transfer' && frm.doc.per_transferred < 100) {
				frm.add_custom_button(__('End Transit'), function() {
					finergy.model.open_mapped_doc({
						method: "capkpi.stock.doctype.stock_entry.stock_entry.make_stock_in_entry",
						frm: frm
					})
				});
			}

			if (frm.doc.per_transferred > 0) {
				frm.add_custom_button(__('Received Stock Entries'), function() {
					finergy.route_options = {
						'outgoing_stock_entry': frm.doc.name,
						'docstatus': ['!=', 2]
					};

					finergy.set_route('List', 'Stock Entry');
				}, __("View"));
			}
		}

		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Purchase Invoice'), function() {
				capkpi.utils.map_current_doc({
					method: "capkpi.accounts.doctype.purchase_invoice.purchase_invoice.make_stock_entry",
					source_doctype: "Purchase Invoice",
					target: frm,
					date_field: "posting_date",
					setters: {
						supplier: frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 1
					}
				})
			}, __("Get Items From"));

			frm.add_custom_button(__('Material Request'), function() {
				const allowed_request_types = ["Material Transfer", "Material Issue", "Customer Provided"];
				const depends_on_condition = "eval:doc.material_request_type==='Customer Provided'";
				const d = capkpi.utils.map_current_doc({
					method: "capkpi.stock.doctype.material_request.material_request.make_stock_entry",
					source_doctype: "Material Request",
					target: frm,
					date_field: "schedule_date",
					setters: [{
						fieldtype: 'Select',
						label: __('Purpose'),
						options: allowed_request_types.join("\n"),
						fieldname: 'material_request_type',
						default: "Material Transfer",
						mandatory: 1,
						change() {
							if (this.value === 'Customer Provided') {
								d.dialog.get_field("customer").set_focus();
							}
						},
					},
					{
						fieldtype: 'Link',
						label: __('Customer'),
						options: 'Customer',
						fieldname: 'customer',
						depends_on: depends_on_condition,
						mandatory_depends_on: depends_on_condition,
					}],
					get_query_filters: {
						docstatus: 1,
						material_request_type: ["in", allowed_request_types],
						status: ["not in", ["Transferred", "Issued", "Cancelled", "Stopped"]]
					}
				})
			}, __("Get Items From"));
		}
		if (frm.doc.docstatus===0 && frm.doc.purpose == "Material Issue") {
			frm.add_custom_button(__('Expired Batches'), function() {
				finergy.call({
					method: "capkpi.stock.doctype.stock_entry.stock_entry.get_expired_batch_items",
					callback: function(r) {
						if (!r.exc && r.message) {
							frm.set_value("items", []);
							r.message.forEach(function(element) {
								let d = frm.add_child("items");
								d.item_code = element.item;
								d.s_warehouse = element.warehouse;
								d.qty = element.qty;
								d.uom = element.stock_uom;
								d.conversion_factor = 1;
								d.batch_no = element.batch_no;
								d.transfer_qty = element.qty;
								frm.refresh_fields();
							});
						}
					}
				});
			}, __("Get Items From"));
		}

		frm.events.show_bom_custom_button(frm);

		if (frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}

		if(frm.doc.docstatus==1 && frm.doc.purpose == "Material Receipt" && frm.get_sum('items', 			'sample_quantity')) {
			frm.add_custom_button(__('Create Sample Retention Stock Entry'), function () {
				frm.trigger("make_retention_stock_entry");
			});
		}

		frm.trigger("setup_quality_inspection");
		attach_bom_items(frm.doc.bom_no)
	},

	before_save: function(frm) {
		frm.doc.items.forEach((item) => {
			item.uom = item.uom || item.stock_uom;
		})
	},

	stock_entry_type: function(frm){
		frm.remove_custom_button('Bill of Materials', "Get Items From");
		frm.events.show_bom_custom_button(frm);
		frm.trigger('add_to_transit');
	},

	purpose: function(frm) {
		frm.trigger('validate_purpose_consumption');
		frm.fields_dict.items.grid.refresh();
		frm.cscript.toggle_related_fields(frm.doc);
	},

	validate_purpose_consumption: function(frm) {
		finergy.call({
			method: "capkpi.manufacturing.doctype.manufacturing_settings.manufacturing_settings.is_material_consumption_enabled",
		}).then(r => {
			if (cint(r.message) == 0
				&& frm.doc.purpose=="Material Consumption for Manufacture") {
				frm.set_value("purpose", 'Manufacture');
				finergy.throw(__('Material Consumption is not set in Manufacturing Settings.'));
			}
		});
	},

	company: function(frm) {
		if(frm.doc.company) {
			var company_doc = finergy.get_doc(":Company", frm.doc.company);
			if(company_doc.default_letter_head) {
				frm.set_value("letter_head", company_doc.default_letter_head);
			}
			frm.trigger("toggle_display_account_head");

			capkpi.accounts.dimensions.update_dimension(frm, frm.doctype);
		}
	},

	set_serial_no: function(frm, cdt, cdn, callback) {
		var d = finergy.model.get_doc(cdt, cdn);
		if(!d.item_code && !d.s_warehouse && !d.qty) return;
		var	args = {
			'item_code'	: d.item_code,
			'warehouse'	: cstr(d.s_warehouse),
			'stock_qty'		: d.transfer_qty
		};
		finergy.call({
			method: "capkpi.stock.get_item_details.get_serial_no",
			args: {"args": args},
			callback: function(r) {
				if (!r.exe && r.message){
					finergy.model.set_value(cdt, cdn, "serial_no", r.message);
				}
				if (callback) {
					callback();
				}
			}
		});
	},

	make_retention_stock_entry: function(frm) {
		finergy.call({
			method: "capkpi.stock.doctype.stock_entry.stock_entry.move_sample_to_retention_warehouse",
			args:{
				"company": frm.doc.company,
				"items": frm.doc.items
			},
			callback: function (r) {
				if (r.message) {
					var doc = finergy.model.sync(r.message)[0];
					finergy.set_route("Form", doc.doctype, doc.name);
				}
				else {
					finergy.msgprint(__("Retention Stock Entry already created or Sample Quantity not provided"));
				}
			}
		});
	},

	toggle_display_account_head: function(frm) {
		var enabled = capkpi.is_perpetual_inventory_enabled(frm.doc.company);
		frm.fields_dict["items"].grid.set_column_disp(["cost_center", "expense_account"], enabled);
	},

	set_basic_rate: function(frm, cdt, cdn) {
		const item = locals[cdt][cdn];
		item.transfer_qty = flt(item.qty) * flt(item.conversion_factor);

		const args = {
			'item_code'			: item.item_code,
			'posting_date'		: frm.doc.posting_date,
			'posting_time'		: frm.doc.posting_time,
			'warehouse'			: cstr(item.s_warehouse) || cstr(item.t_warehouse),
			'serial_no'			: item.serial_no,
			'batch_no'          : item.batch_no,
			'company'			: frm.doc.company,
			'qty'				: item.s_warehouse ? -1*flt(item.transfer_qty) : flt(item.transfer_qty),
			'voucher_type'		: frm.doc.doctype,
			'voucher_no'		: item.name,
			'allow_zero_valuation': 1,
		};

		if (item.item_code || item.serial_no) {
			finergy.call({
				method: "capkpi.stock.utils.get_incoming_rate",
				args: {
					args: args
				},
				callback: function(r) {
					finergy.model.set_value(cdt, cdn, 'basic_rate', (r.message || 0.0));
					frm.events.calculate_basic_amount(frm, item);
				}
			});
		}
	},

	get_warehouse_details: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		if(!child.bom_no) {
			finergy.call({
				method: "capkpi.stock.doctype.stock_entry.stock_entry.get_warehouse_details",
				args: {
					"args": {
						'item_code': child.item_code,
						'warehouse': cstr(child.s_warehouse) || cstr(child.t_warehouse),
						'transfer_qty': child.transfer_qty,
						'serial_no': child.serial_no,
						'batch_no': child.batch_no,
						'qty': child.s_warehouse ? -1* child.transfer_qty : child.transfer_qty,
						'posting_date': frm.doc.posting_date,
						'posting_time': frm.doc.posting_time,
						'company': frm.doc.company,
						'voucher_type': frm.doc.doctype,
						'voucher_no': child.name,
						'allow_zero_valuation': 1
					}
				},
				callback: function(r) {
					if (!r.exc) {
						["actual_qty", "basic_rate"].forEach((field) => {
							finergy.model.set_value(cdt, cdn, field, (r.message[field] || 0.0));
						});
						frm.events.calculate_basic_amount(frm, child);
					}
				}
			});
		}
	},

	show_bom_custom_button: function(frm){
		if (frm.doc.docstatus === 0 &&
			['Material Issue', 'Material Receipt', 'Material Transfer', 'Send to Subcontractor'].includes(frm.doc.purpose)) {
			frm.add_custom_button(__('Bill of Materials'), function() {
				frm.events.get_items_from_bom(frm);
			}, __("Get Items From"));
		}
	},

	get_items_from_bom: function(frm) {
		let filters = function(){
			return {filters: { docstatus:1 }};
		}

		let fields = [
			{"fieldname":"bom", "fieldtype":"Link", "label":__("BOM"),
			options:"BOM", reqd: 1, get_query: filters()},
			{"fieldname":"source_warehouse", "fieldtype":"Link", "label":__("Source Warehouse"),
			options:"Warehouse"},
			{"fieldname":"target_warehouse", "fieldtype":"Link", "label":__("Target Warehouse"),
			options:"Warehouse"},
			{"fieldname":"qty", "fieldtype":"Float", "label":__("Quantity"),
			reqd: 1, "default": 1},
			{"fieldname":"fetch_exploded", "fieldtype":"Check",
			"label":__("Fetch exploded BOM (including sub-assemblies)"), "default":1},
			{"fieldname":"fetch", "label":__("Get Items from BOM"), "fieldtype":"Button"}
		]

		// Exclude field 'Target Warehouse' in case of Material Issue
		if (frm.doc.purpose == 'Material Issue'){
			fields.splice(2,1);
		}
		// Exclude field 'Source Warehouse' in case of Material Receipt
		else if(frm.doc.purpose == 'Material Receipt'){
			fields.splice(1,1);
		}

		let d = new finergy.ui.Dialog({
			title: __("Get Items from BOM"),
			fields: fields
		});
		d.get_input("fetch").on("click", function() {
			let values = d.get_values();
			if(!values) return;
			values["company"] = frm.doc.company;
			if(!frm.doc.company) finergy.throw(__("Company field is required"));
			finergy.call({
				method: "capkpi.manufacturing.doctype.bom.bom.get_bom_items",
				args: values,
				callback: function(r) {
					if (!r.message) {
						finergy.throw(__("BOM does not contain any stock item"));
					} else {
						capkpi.utils.remove_empty_first_row(frm, "items");
						$.each(r.message, function(i, item) {
							let d = finergy.model.add_child(cur_frm.doc, "Stock Entry Detail", "items");
							d.item_code = item.item_code;
							d.item_name = item.item_name;
							d.item_group = item.item_group;
							d.s_warehouse = values.source_warehouse;
							d.t_warehouse = values.target_warehouse;
							d.uom = item.stock_uom;
							d.stock_uom = item.stock_uom;
							d.conversion_factor = item.conversion_factor ? item.conversion_factor : 1;
							d.qty = item.qty;
							d.expense_account = item.expense_account;
							d.project = item.project;
							frm.events.set_basic_rate(frm, d.doctype, d.name);
						});
					}
					d.hide();
					refresh_field("items");
				}
			});

		});
		d.show();
	},

	calculate_basic_amount: function(frm, item) {
		item.basic_amount = flt(flt(item.transfer_qty) * flt(item.basic_rate),
			precision("basic_amount", item));
		frm.events.calculate_total_additional_costs(frm);
	},

	calculate_total_additional_costs: function(frm) {
		const total_additional_costs = finergy.utils.sum(
			(frm.doc.additional_costs || []).map(function(c) { return flt(c.base_amount); })
		);

		frm.set_value("total_additional_costs",
			flt(total_additional_costs, precision("total_additional_costs")));
	},

	source_warehouse_address: function(frm) {
		capkpi.utils.get_address_display(frm, 'source_warehouse_address', 'source_address_display', false);
	},

	target_warehouse_address: function(frm) {
		capkpi.utils.get_address_display(frm, 'target_warehouse_address', 'target_address_display', false);
	},

	add_to_transit: function(frm) {
		if(frm.doc.purpose=='Material Transfer') {
			var filters = {
				'is_group': 0,
				'company': frm.doc.company
			}

			if(frm.doc.add_to_transit){
				filters['warehouse_type'] = 'Transit';
				frm.set_value('to_warehouse', '');
				frm.trigger('set_transit_warehouse');
			}

			frm.fields_dict.to_warehouse.get_query = function() {
				return {
					filters:filters
				};
			};
		}
	},

	set_transit_warehouse: function(frm) {
		if(frm.doc.add_to_transit && frm.doc.purpose == 'Material Transfer' && !frm.doc.to_warehouse
			&& frm.doc.from_warehouse) {
			let dt = frm.doc.from_warehouse ? 'Warehouse' : 'Company';
			let dn = frm.doc.from_warehouse ? frm.doc.from_warehouse : frm.doc.company;
			finergy.db.get_value(dt, dn, 'default_in_transit_warehouse', (r) => {
				if (r.default_in_transit_warehouse) {
					frm.set_value('to_warehouse', r.default_in_transit_warehouse);
				}
			});
		}
	},

	apply_putaway_rule: function (frm) {
		if (frm.doc.apply_putaway_rule) capkpi.apply_putaway_rule(frm, frm.doc.purpose);
	},

	purchase_order: (frm) => {
		if (frm.doc.purchase_order) {
			frm.set_value("subcontracting_order", "");
		}
	},

	subcontracting_order: (frm) => {
		if (frm.doc.subcontracting_order) {
			frm.set_value("purchase_order", "");
			capkpi.utils.map_current_doc({
				method: 'capkpi.stock.doctype.stock_entry.stock_entry.get_items_from_subcontracting_order',
				source_name: frm.doc.subcontracting_order,
				target_doc: frm,
				freeze: true,
			});
		}
	},
});

finergy.ui.form.on('Stock Entry Detail', {
	qty: function(frm, cdt, cdn) {
		frm.events.set_serial_no(frm, cdt, cdn, () => {
			frm.events.set_basic_rate(frm, cdt, cdn);
		});
	},

	conversion_factor: function(frm, cdt, cdn) {
		frm.events.set_basic_rate(frm, cdt, cdn);
	},

	s_warehouse: function(frm, cdt, cdn) {
		frm.events.set_serial_no(frm, cdt, cdn, () => {
			frm.events.get_warehouse_details(frm, cdt, cdn);
		});

		// set allow_zero_valuation_rate to 0 if s_warehouse is selected.
		let item = finergy.get_doc(cdt, cdn);
		if (item.s_warehouse) {
			finergy.model.set_value(cdt, cdn, "allow_zero_valuation_rate", 0);
		}
	},

	t_warehouse: function(frm, cdt, cdn) {
		frm.events.get_warehouse_details(frm, cdt, cdn);
	},

	basic_rate: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];
		frm.events.calculate_basic_amount(frm, item);
	},

	uom: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.uom && d.item_code){
			return finergy.call({
				method: "capkpi.stock.doctype.stock_entry.stock_entry.get_uom_details",
				args: {
					item_code: d.item_code,
					uom: d.uom,
					qty: d.qty
				},
				callback: function(r) {
					if(r.message) {
						finergy.model.set_value(cdt, cdn, r.message);
					}
				}
			});
		}
	},

	item_code: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.item_code) {
			var args = {
				'item_code'			: d.item_code,
				'warehouse'			: cstr(d.s_warehouse) || cstr(d.t_warehouse),
				'transfer_qty'		: d.transfer_qty,
				'serial_no'		: d.serial_no,
				'batch_no'      : d.batch_no,
				'bom_no'		: d.bom_no,
				'expense_account'	: d.expense_account,
				'cost_center'		: d.cost_center,
				'company'		: frm.doc.company,
				'qty'			: d.qty,
				'voucher_type'		: frm.doc.doctype,
				'voucher_no'		: d.name,
				'allow_zero_valuation': 1,
			};

			return finergy.call({
				doc: frm.doc,
				method: "get_item_details",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							if (v) {
								finergy.model.set_value(cdt, cdn, k, v); // qty and it's subsequent fields weren't triggered
							}
						});
						refresh_field("items");

						let no_batch_serial_number_value = !d.serial_no;
						if (d.has_batch_no && !d.has_serial_no) {
							// check only batch_no for batched item
							no_batch_serial_number_value = !d.batch_no;
						}

						if (no_batch_serial_number_value && !finergy.flags.hide_serial_batch_dialog) {
							capkpi.stock.select_batch_and_serial_no(frm, d);
						}
					}
				}
			});
		}
	},
	expense_account: function(frm, cdt, cdn) {
		capkpi.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "expense_account");
	},
	cost_center: function(frm, cdt, cdn) {
		capkpi.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "cost_center");
	},
	sample_quantity: function(frm, cdt, cdn) {
		validate_sample_quantity(frm, cdt, cdn);
	},
	batch_no: function(frm, cdt, cdn) {
		validate_sample_quantity(frm, cdt, cdn);
	},
});

var validate_sample_quantity = function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.sample_quantity && frm.doc.purpose == "Material Receipt") {
		finergy.call({
			method: 'capkpi.stock.doctype.stock_entry.stock_entry.validate_sample_quantity',
			args: {
				batch_no: d.batch_no,
				item_code: d.item_code,
				sample_quantity: d.sample_quantity,
				qty: d.transfer_qty
			},
			callback: (r) => {
				finergy.model.set_value(cdt, cdn, "sample_quantity", r.message);
			}
		});
	}
};

finergy.ui.form.on('Landed Cost Taxes and Charges', {
	amount: function(frm, cdt, cdn) {
		frm.events.set_base_amount(frm, cdt, cdn);

	},

	expense_account: function(frm, cdt, cdn) {
		frm.events.set_account_currency(frm, cdt, cdn);
	}
});

capkpi.stock.StockEntry = class StockEntry extends capkpi.stock.StockController {
	setup() {
		var me = this;

		this.setup_posting_date_time_check();

		this.frm.fields_dict.bom_no.get_query = function() {
			return {
				filters:{
					"docstatus": 1,
					"is_active": 1
				}
			};
		};

		this.frm.fields_dict.items.grid.get_field('item_code').get_query = function() {
			return capkpi.queries.item({is_stock_item: 1});
		};

		this.frm.set_query("purchase_order", function() {
			return {
				"filters": {
					"docstatus": 1,
					"is_old_subcontracting_flow": 1,
					"company": me.frm.doc.company
				}
			};
		});

		this.frm.set_query("subcontracting_order", function() {
			return {
				"filters": {
					"docstatus": 1,
					"company": me.frm.doc.company
				}
			};
		});

		if(me.frm.doc.company && capkpi.is_perpetual_inventory_enabled(me.frm.doc.company)) {
			this.frm.add_fetch("company", "stock_adjustment_account", "expense_account");
		}

		this.frm.fields_dict.items.grid.get_field('expense_account').get_query = function() {
			if (capkpi.is_perpetual_inventory_enabled(me.frm.doc.company)) {
				return {
					filters: {
						"company": me.frm.doc.company,
						"is_group": 0
					}
				}
			}
		}

		if (me.frm.doc.purchase_order) {
			this.frm.add_fetch("purchase_order", "supplier", "supplier");
		}
		else {
			this.frm.add_fetch("subcontracting_order", "supplier", "supplier");
		}

		finergy.dynamic_link = { doc: this.frm.doc, fieldname: 'supplier', doctype: 'Supplier' }
		this.frm.set_query("supplier_address", capkpi.queries.address_query)
	}

	onload_post_render() {
		var me = this;
		this.set_default_account(function() {
			if(me.frm.doc.__islocal && me.frm.doc.company && !me.frm.doc.amended_from) {
				me.frm.trigger("company");
			}
		});

		this.frm.get_field("items").grid.set_multiple_add("item_code", "qty");
	}

	refresh() {
		var me = this;
		capkpi.toggle_naming_series();
		this.toggle_related_fields(this.frm.doc);
		this.toggle_enable_bom();
		this.show_stock_ledger();
		if (this.frm.doc.docstatus===1 && capkpi.is_perpetual_inventory_enabled(this.frm.doc.company)) {
			this.show_general_ledger();
		}
		capkpi.hide_company();
		capkpi.utils.add_item(this.frm);
	}

	scan_barcode() {
		const barcode_scanner = new capkpi.utils.BarcodeScanner({frm:this.frm});
		barcode_scanner.process_scan();
	}

	on_submit() {
		this.clean_up();
	}

	after_cancel() {
		this.clean_up();
	}

	set_default_account(callback) {
		var me = this;

		if(this.frm.doc.company && capkpi.is_perpetual_inventory_enabled(this.frm.doc.company)) {
			return this.frm.call({
				method: "capkpi.accounts.utils.get_company_default",
				args: {
					"fieldname": "stock_adjustment_account",
					"company": this.frm.doc.company
				},
				callback: function(r) {
					if (!r.exc) {
						$.each(me.frm.doc.items || [], function(i, d) {
							if(!d.expense_account) d.expense_account = r.message;
						});
						if(callback) callback();
					}
				}
			});
		}
	}

	clean_up() {
		// Clear Work Order record from locals, because it is updated via Stock Entry
		if(this.frm.doc.work_order &&
			in_list(["Manufacture", "Material Transfer for Manufacture", "Material Consumption for Manufacture"],
				this.frm.doc.purpose)) {
			finergy.model.remove_from_locals("Work Order",
				this.frm.doc.work_order);
		}
	}

	fg_completed_qty() {
		this.get_items();
	}

	get_items() {
		var me = this;
		if(!this.frm.doc.fg_completed_qty || !this.frm.doc.bom_no)
			finergy.throw(__("BOM and Manufacturing Quantity are required"));

		if(this.frm.doc.work_order || this.frm.doc.bom_no) {
			// if work order / bom is mentioned, get items
			return this.frm.call({
				doc: me.frm.doc,
				freeze: true,
				method: "get_items",
				callback: function(r) {
					if(!r.exc) refresh_field("items");
					if(me.frm.doc.bom_no) attach_bom_items(me.frm.doc.bom_no)
				}
			});
		}
	}

	work_order() {
		var me = this;
		this.toggle_enable_bom();
		if(!me.frm.doc.work_order || me.frm.doc.job_card) {
			return;
		}

		return finergy.call({
			method: "capkpi.stock.doctype.stock_entry.stock_entry.get_work_order_details",
			args: {
				work_order: me.frm.doc.work_order,
				company: me.frm.doc.company
			},
			callback: function(r) {
				if (!r.exc) {
					$.each(["from_bom", "bom_no", "fg_completed_qty", "use_multi_level_bom"], function(i, field) {
						me.frm.set_value(field, r.message[field]);
					})

					if (me.frm.doc.purpose == "Material Transfer for Manufacture" && !me.frm.doc.to_warehouse)
						me.frm.set_value("to_warehouse", r.message["wip_warehouse"]);


					if (me.frm.doc.purpose == "Manufacture" || me.frm.doc.purpose == "Material Consumption for Manufacture" ) {
						if (me.frm.doc.purpose == "Manufacture") {
							if (!me.frm.doc.to_warehouse) me.frm.set_value("to_warehouse", r.message["fg_warehouse"]);
						}
						if (!me.frm.doc.from_warehouse) me.frm.set_value("from_warehouse", r.message["wip_warehouse"]);
					}
					me.get_items();
				}
			}
		});
	}

	toggle_enable_bom() {
		this.frm.toggle_enable("bom_no", !!!this.frm.doc.work_order);
	}

	add_excise_button() {
		if(finergy.boot.sysdefaults.country === "India")
			this.frm.add_custom_button(__("Excise Invoice"), function() {
				var excise = finergy.model.make_new_doc_and_get_name('Journal Entry');
				excise = locals['Journal Entry'][excise];
				excise.voucher_type = 'Excise Entry';
				finergy.set_route('Form', 'Journal Entry', excise.name);
			}, __('Create'));
	}

	items_add(doc, cdt, cdn) {
		var row = finergy.get_doc(cdt, cdn);

		if (!(row.expense_account && row.cost_center)) {
			this.frm.script_manager.copy_from_first_row("items", row, ["expense_account", "cost_center"]);
		}

		if(!row.s_warehouse) row.s_warehouse = this.frm.doc.from_warehouse;
		if(!row.t_warehouse) row.t_warehouse = this.frm.doc.to_warehouse;
	}

	from_warehouse(doc) {
		this.frm.trigger('set_transit_warehouse');
		this.set_warehouse_in_children(doc.items, "s_warehouse", doc.from_warehouse);
	}

	to_warehouse(doc) {
		this.set_warehouse_in_children(doc.items, "t_warehouse", doc.to_warehouse);
	}

	set_warehouse_in_children(child_table, warehouse_field, warehouse) {
		let transaction_controller = new capkpi.TransactionController();
		transaction_controller.autofill_warehouse(child_table, warehouse_field, warehouse);
	}

	items_on_form_rendered(doc, grid_row) {
		capkpi.setup_serial_or_batch_no();
	}

	toggle_related_fields(doc) {
		this.frm.toggle_enable("from_warehouse", doc.purpose!='Material Receipt');
		this.frm.toggle_enable("to_warehouse", doc.purpose!='Material Issue');

		this.frm.fields_dict["items"].grid.set_column_disp("retain_sample", doc.purpose=='Material Receipt');
		this.frm.fields_dict["items"].grid.set_column_disp("sample_quantity", doc.purpose=='Material Receipt');

		this.frm.cscript.toggle_enable_bom();

		if (doc.purpose == 'Send to Subcontractor') {
			doc.customer = doc.customer_name = doc.customer_address =
				doc.delivery_note_no = doc.sales_invoice_no = null;
		} else {
			doc.customer = doc.customer_name = doc.customer_address =
				doc.delivery_note_no = doc.sales_invoice_no = doc.supplier =
				doc.supplier_name = doc.supplier_address = doc.purchase_receipt_no =
				doc.address_display = null;
		}
		if(doc.purpose == "Material Receipt") {
			this.frm.set_value("from_bom", 0);
		}

		// Addition costs based on purpose
		this.frm.toggle_display(["additional_costs", "total_additional_costs", "additional_costs_section"],
			doc.purpose!='Material Issue');

		this.frm.fields_dict["items"].grid.set_column_disp("additional_cost", doc.purpose!='Material Issue');
	}

	supplier(doc) {
		capkpi.utils.get_party_details(this.frm, null, null, null);
	}
};

capkpi.stock.select_batch_and_serial_no = (frm, item) => {
	let get_warehouse_type_and_name = (item) => {
		let value = '';
		if(frm.fields_dict.from_warehouse.disp_status === "Write") {
			value = cstr(item.s_warehouse) || '';
			return {
				type: 'Source Warehouse',
				name: value
			};
		} else {
			value = cstr(item.t_warehouse) || '';
			return {
				type: 'Target Warehouse',
				name: value
			};
		}
	}

	if(item && !item.has_serial_no && !item.has_batch_no) return;
	if (frm.doc.purpose === 'Material Receipt') return;

	finergy.require("assets/capkpi/js/utils/serial_no_batch_selector.js", function() {
		new capkpi.SerialNoBatchSelector({
			frm: frm,
			item: item,
			warehouse_details: get_warehouse_type_and_name(item),
		});
	});

}

function attach_bom_items(bom_no) {
	if (!bom_no) {
		return
	}

	if (check_should_not_attach_bom_items(bom_no)) return
	finergy.db.get_doc("BOM",bom_no).then(bom => {
		const {name, items} = bom
		capkpi.stock.bom = {name, items:{}}
		items.forEach(item => {
			capkpi.stock.bom.items[item.item_code] = item;
		});
	});
}

function check_should_not_attach_bom_items(bom_no) {
  return (
	bom_no === undefined ||
	(capkpi.stock.bom && capkpi.stock.bom.name === bom_no)
  );
}

extend_cscript(cur_frm.cscript, new capkpi.stock.StockEntry({frm: cur_frm}));