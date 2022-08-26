# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

from finergy import _


def get_data():
	return {
		"fieldname": "course_schedule",
		"transactions": [{"label": _("Attendance"), "items": ["Student Attendance"]}],
	}
