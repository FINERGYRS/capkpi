# Copyright (c) 2018, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.setup.doctype.company.company import install_country_fixtures


def execute():
	finergy.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in finergy.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
