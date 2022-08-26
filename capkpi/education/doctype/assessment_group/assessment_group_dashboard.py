# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

from finergy import _


def get_data():
	return {
		"fieldname": "assessment_group",
		"transactions": [{"label": _("Assessment"), "items": ["Assessment Plan", "Assessment Result"]}],
	}
