# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():

	if finergy.db.exists("DocType", "Bank Reconciliation Detail") and finergy.db.exists(
		"DocType", "Bank Clearance Detail"
	):

		finergy.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
