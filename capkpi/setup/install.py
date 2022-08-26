# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.custom.doctype.custom_field.custom_field import create_custom_field
from finergy.desk.page.setup_wizard.setup_wizard import add_all_roles_to
from finergy.installer import update_site_config
from finergy.utils import cint
from six import iteritems

from capkpi.accounts.doctype.cash_flow_mapper.default_cash_flow_mapper import DEFAULT_MAPPERS
from capkpi.setup.default_energy_point_rules import get_default_energy_point_rules

from .default_success_action import get_default_success_action

default_mail_footer = """<div style="padding: 7px; text-align: right; color: #888"><small>Sent via
	<a style="color: #888" href="http://capkpi.org">CapKPI</a></div>"""


def after_install():
	finergy.get_doc({"doctype": "Role", "role_name": "Analytics"}).insert()
	set_single_defaults()
	create_compact_item_print_custom_field()
	create_print_uom_after_qty_custom_field()
	create_print_zero_amount_taxes_custom_field()
	add_all_roles_to("Administrator")
	create_default_cash_flow_mapper_templates()
	create_default_success_action()
	create_default_energy_point_rules()
	add_company_to_session_defaults()
	add_standard_navbar_items()
	add_app_name()
	add_non_standard_user_types()
	finergy.db.commit()


def check_setup_wizard_not_completed():
	if cint(finergy.db.get_single_value("System Settings", "setup_complete") or 0):
		message = """CapKPI can only be installed on a fresh site where the setup wizard is not completed.
You can reinstall this site (after saving your data) using: bench --site [sitename] reinstall"""
		finergy.throw(message)  # nosemgrep


def set_single_defaults():
	for dt in (
		"Accounts Settings",
		"Print Settings",
		"HR Settings",
		"Buying Settings",
		"Selling Settings",
		"Stock Settings",
	):
		default_values = finergy.db.sql(
			"""select fieldname, `default` from `tabDocField`
			where parent=%s""",
			dt,
		)
		if default_values:
			try:
				b = finergy.get_doc(dt, dt)
				for fieldname, value in default_values:
					b.set(fieldname, value)
				b.save()
			except finergy.MandatoryError:
				pass
			except finergy.ValidationError:
				pass

	finergy.db.set_default("date_format", "dd-mm-yyyy")


def create_compact_item_print_custom_field():
	create_custom_field(
		"Print Settings",
		{
			"label": _("Compact Item Print"),
			"fieldname": "compact_item_print",
			"fieldtype": "Check",
			"default": 1,
			"insert_after": "with_letterhead",
		},
	)


def create_print_uom_after_qty_custom_field():
	create_custom_field(
		"Print Settings",
		{
			"label": _("Print UOM after Quantity"),
			"fieldname": "print_uom_after_quantity",
			"fieldtype": "Check",
			"default": 0,
			"insert_after": "compact_item_print",
		},
	)


def create_print_zero_amount_taxes_custom_field():
	create_custom_field(
		"Print Settings",
		{
			"label": _("Print taxes with zero amount"),
			"fieldname": "print_taxes_with_zero_amount",
			"fieldtype": "Check",
			"default": 0,
			"insert_after": "allow_print_for_cancelled",
		},
	)


def create_default_cash_flow_mapper_templates():
	for mapper in DEFAULT_MAPPERS:
		if not finergy.db.exists("Cash Flow Mapper", mapper["section_name"]):
			doc = finergy.get_doc(mapper)
			doc.insert(ignore_permissions=True)


def create_default_success_action():
	for success_action in get_default_success_action():
		if not finergy.db.exists("Success Action", success_action.get("ref_doctype")):
			doc = finergy.get_doc(success_action)
			doc.insert(ignore_permissions=True)


def create_default_energy_point_rules():

	for rule in get_default_energy_point_rules():
		# check if any rule for ref. doctype exists
		rule_exists = finergy.db.exists(
			"Energy Point Rule", {"reference_doctype": rule.get("reference_doctype")}
		)
		if rule_exists:
			continue
		doc = finergy.get_doc(rule)
		doc.insert(ignore_permissions=True)


def add_company_to_session_defaults():
	settings = finergy.get_single("Session Default Settings")
	settings.append("session_defaults", {"ref_doctype": "Company"})
	settings.save()


def add_standard_navbar_items():
	navbar_settings = finergy.get_single("Navbar Settings")

	capkpi_navbar_items = [
		{
			"item_label": "Documentation",
			"item_type": "Route",
			"route": "https://capkpi.com/docs/user/manual",
			"is_standard": 1,
		},
		{
			"item_label": "User Forum",
			"item_type": "Route",
			"route": "https://discuss.capkpi.com",
			"is_standard": 1,
		},
		{
			"item_label": "Report an Issue",
			"item_type": "Route",
			"route": "https://github.com/finergyrs/capkpi/issues",
			"is_standard": 1,
		},
	]

	current_navbar_items = navbar_settings.help_dropdown
	navbar_settings.set("help_dropdown", [])

	for item in capkpi_navbar_items:
		current_labels = [item.get("item_label") for item in current_navbar_items]
		if not item.get("item_label") in current_labels:
			navbar_settings.append("help_dropdown", item)

	for item in current_navbar_items:
		navbar_settings.append(
			"help_dropdown",
			{
				"item_label": item.item_label,
				"item_type": item.item_type,
				"route": item.route,
				"action": item.action,
				"is_standard": item.is_standard,
				"hidden": item.hidden,
			},
		)

	navbar_settings.save()


def add_app_name():
	finergy.db.set_value("System Settings", None, "app_name", "CapKPI")


def add_non_standard_user_types():
	user_types = get_user_types_data()

	user_type_limit = {}
	for user_type, data in iteritems(user_types):
		user_type_limit.setdefault(finergy.scrub(user_type), 10)

	update_site_config("user_type_doctype_limit", user_type_limit)

	for user_type, data in iteritems(user_types):
		create_custom_role(data)
		create_user_type(user_type, data)


def get_user_types_data():
	return {
		"Employee Self Service": {
			"role": "Employee Self Service",
			"apply_user_permission_on": "Employee",
			"user_id_field": "user_id",
			"doctypes": {
				"Salary Slip": ["read"],
				"Employee": ["read", "write"],
				"Expense Claim": ["read", "write", "create", "delete"],
				"Leave Application": ["read", "write", "create", "delete"],
				"Attendance Request": ["read", "write", "create", "delete"],
				"Compensatory Leave Request": ["read", "write", "create", "delete"],
				"Employee Tax Exemption Declaration": ["read", "write", "create", "delete"],
				"Employee Tax Exemption Proof Submission": ["read", "write", "create", "delete"],
				"Timesheet": ["read", "write", "create", "delete", "submit", "cancel", "amend"],
			},
		}
	}


def create_custom_role(data):
	if data.get("role") and not finergy.db.exists("Role", data.get("role")):
		finergy.get_doc(
			{"doctype": "Role", "role_name": data.get("role"), "desk_access": 1, "is_custom": 1}
		).insert(ignore_permissions=True)


def create_user_type(user_type, data):
	if finergy.db.exists("User Type", user_type):
		doc = finergy.get_cached_doc("User Type", user_type)
		doc.user_doctypes = []
	else:
		doc = finergy.new_doc("User Type")
		doc.update(
			{
				"name": user_type,
				"role": data.get("role"),
				"user_id_field": data.get("user_id_field"),
				"apply_user_permission_on": data.get("apply_user_permission_on"),
			}
		)

	create_role_permissions_for_doctype(doc, data)
	doc.save(ignore_permissions=True)


def create_role_permissions_for_doctype(doc, data):
	for doctype, perms in iteritems(data.get("doctypes")):
		args = {"document_type": doctype}
		for perm in perms:
			args[perm] = 1

		doc.append("user_doctypes", args)


def update_select_perm_after_install():
	if not finergy.flags.update_select_perm_after_migrate:
		return

	finergy.flags.ignore_select_perm = False
	for row in finergy.get_all("User Type", filters={"is_standard": 0}):
		print("Updating user type :- ", row.name)
		doc = finergy.get_doc("User Type", row.name)
		doc.save()

	finergy.flags.update_select_perm_after_migrate = False
