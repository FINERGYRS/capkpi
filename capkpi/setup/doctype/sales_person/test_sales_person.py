# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

test_dependencies = ["Employee"]

import finergy

test_records = finergy.get_test_records("Sales Person")

test_ignore = ["Item Group"]
