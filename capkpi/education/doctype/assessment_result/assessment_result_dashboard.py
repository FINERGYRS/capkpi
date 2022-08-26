# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

from finergy import _


def get_data():
	return {
		"reports": [
			{"label": _("Reports"), "items": ["Final Assessment Grades", "Course wise Assessment Report"]}
		]
	}
