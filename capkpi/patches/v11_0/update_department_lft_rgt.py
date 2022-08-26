import finergy
from finergy import _
from finergy.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	finergy.reload_doc("hr", "doctype", "department")
	if not finergy.db.exists("Department", _("All Departments")):
		finergy.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	finergy.db.sql(
		"""update `tabDepartment` set parent_department = '{0}'
		where is_group = 0""".format(
			_("All Departments")
		)
	)

	rebuild_tree("Department", "parent_department")
