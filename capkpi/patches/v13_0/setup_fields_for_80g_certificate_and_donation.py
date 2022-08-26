import finergy

from capkpi.regional.india.setup import make_custom_fields


def execute():
	if finergy.get_all("Company", filters={"country": "India"}):
		finergy.reload_doc("accounts", "doctype", "POS Invoice")
		finergy.reload_doc("accounts", "doctype", "POS Invoice Item")

		make_custom_fields()

		if not finergy.db.exists("Party Type", "Donor"):
			finergy.get_doc(
				{"doctype": "Party Type", "party_type": "Donor", "account_type": "Receivable"}
			).insert(ignore_permissions=True)
