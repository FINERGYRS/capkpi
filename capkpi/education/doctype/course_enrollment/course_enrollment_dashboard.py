# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

from finergy import _


def get_data():
	return {
		"fieldname": "enrollment",
		"transactions": [{"label": _("Activity"), "items": ["Course Activity", "Quiz Activity"]}],
	}
