import finergy
from six import iteritems


def get_context(context):
	context.no_cache = 1
	party = finergy.form_dict.party
	context.party_name = party

	try:
		update_gstin(context)
	except finergy.ValidationError:
		context.invalid_gstin = 1

	party_type = "Customer"
	party_name = finergy.db.get_value("Customer", party)

	if not party_name:
		party_type = "Supplier"
		party_name = finergy.db.get_value("Supplier", party)

	if not party_name:
		context.not_found = 1
		return

	context.party = finergy.get_doc(party_type, party_name)
	context.party.onload()


def update_gstin(context):
	dirty = False
	for key, value in iteritems(finergy.form_dict):
		if key != "party":
			address_name = finergy.get_value("Address", key)
			if address_name:
				address = finergy.get_doc("Address", address_name)
				address.gstin = value.upper()
				address.save(ignore_permissions=True)
				dirty = True

	if dirty:
		finergy.db.commit()
		context.updated = True
