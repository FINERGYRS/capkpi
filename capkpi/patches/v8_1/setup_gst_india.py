import finergy
from finergy.email import sendmail_to_system_managers


def execute():
	finergy.reload_doc("stock", "doctype", "item")
	finergy.reload_doc("stock", "doctype", "customs_tariff_number")
	finergy.reload_doc("accounts", "doctype", "payment_terms_template")
	finergy.reload_doc("accounts", "doctype", "payment_schedule")

	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	finergy.reload_doc("regional", "doctype", "gst_settings")
	finergy.reload_doc("regional", "doctype", "gst_hsn_code")

	for report_name in (
		"GST Sales Register",
		"GST Purchase Register",
		"GST Itemised Sales Register",
		"GST Itemised Purchase Register",
	):

		finergy.reload_doc("regional", "report", finergy.scrub(report_name))

	from capkpi.regional.india.setup import setup

	delete_custom_field_tax_id_if_exists()
	setup(patch=True)
	send_gst_update_email()


def delete_custom_field_tax_id_if_exists():
	for field in finergy.db.sql_list(
		"""select name from `tabCustom Field` where fieldname='tax_id'
		and dt in ('Sales Order', 'Sales Invoice', 'Delivery Note')"""
	):
		finergy.delete_doc("Custom Field", field, ignore_permissions=True)
		finergy.db.commit()


def send_gst_update_email():
	message = """Hello,

<p>CapKPI is now GST Ready!</p>

<p>To start making GST Invoices from 1st of July, you just need to create new Tax Accounts,
Templates and update your Customer's and Supplier's GST Numbers.</p>

<p>Please refer {gst_document_link} to know more about how to setup and implement GST in CapKPI.</p>

<p>Please contact us at support@capkpi.com, if you have any questions.</p>

<p>Thanks,</p>
CapKPI Team.
	""".format(
		gst_document_link="<a href='http://finergy.github.io/capkpi/user/manual/en/regional/india/'> CapKPI GST Document </a>"
	)

	try:
		sendmail_to_system_managers("[Important] CapKPI GST updates", message)
	except Exception as e:
		pass
