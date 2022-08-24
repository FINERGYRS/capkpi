import finergy
from finergy.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if finergy.db.exists("DocType", "Asset Settings"):
		finergy.reload_doctype("Asset Category")
		cwip_value = finergy.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		finergy.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		finergy.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		finergy.delete_doc_if_exists("DocType", "Asset Settings")
