# Copyright (c) 2015, ESS LLP and Contributors
# See license.txt

import unittest

import finergy

from capkpi.healthcare.doctype.patient_appointment.test_patient_appointment import create_patient


class TestPatient(unittest.TestCase):
	def test_customer_created(self):
		finergy.db.sql("""delete from `tabPatient`""")
		finergy.db.set_value("Healthcare Settings", None, "link_customer_to_patient", 1)
		patient = create_patient()
		self.assertTrue(finergy.db.get_value("Patient", patient, "customer"))

	def test_patient_registration(self):
		finergy.db.sql("""delete from `tabPatient`""")
		settings = finergy.get_single("Healthcare Settings")
		settings.collect_registration_fee = 1
		settings.registration_fee = 500
		settings.save()

		patient = create_patient()
		patient = finergy.get_doc("Patient", patient)
		self.assertEqual(patient.status, "Disabled")

		# check sales invoice and patient status
		result = patient.invoice_patient_registration()
		self.assertTrue(finergy.db.exists("Sales Invoice", result.get("invoice")))
		self.assertTrue(patient.status, "Active")

		settings.collect_registration_fee = 0
		settings.save()

	def test_patient_contact(self):
		finergy.db.sql("""delete from `tabPatient` where name like '_Test Patient%'""")
		finergy.db.sql("""delete from `tabCustomer` where name like '_Test Patient%'""")
		finergy.db.sql("""delete from `tabContact` where name like'_Test Patient%'""")
		finergy.db.sql("""delete from `tabDynamic Link` where parent like '_Test Patient%'""")

		patient = create_patient(
			patient_name="_Test Patient Contact", email="test-patient@example.com", mobile="+91 0000000001"
		)
		customer = finergy.db.get_value("Patient", patient, "customer")
		self.assertTrue(customer)
		self.assertTrue(
			finergy.db.exists(
				"Dynamic Link", {"parenttype": "Contact", "link_doctype": "Patient", "link_name": patient}
			)
		)
		self.assertTrue(
			finergy.db.exists(
				"Dynamic Link", {"parenttype": "Contact", "link_doctype": "Customer", "link_name": customer}
			)
		)

		# a second patient linking with same customer
		new_patient = create_patient(
			email="test-patient@example.com", mobile="+91 0000000009", customer=customer
		)
		self.assertTrue(
			finergy.db.exists(
				"Dynamic Link", {"parenttype": "Contact", "link_doctype": "Patient", "link_name": new_patient}
			)
		)
		self.assertTrue(
			finergy.db.exists(
				"Dynamic Link", {"parenttype": "Contact", "link_doctype": "Customer", "link_name": customer}
			)
		)

	def test_patient_user(self):
		finergy.db.sql("""delete from `tabUser` where email='test-patient-user@example.com'""")
		finergy.db.sql("""delete from `tabDynamic Link` where parent like '_Test Patient%'""")
		finergy.db.sql("""delete from `tabPatient` where name like '_Test Patient%'""")

		patient = create_patient(
			patient_name="_Test Patient User",
			email="test-patient-user@example.com",
			mobile="+91 0000000009",
			create_user=True,
		)
		user = finergy.db.get_value("Patient", patient, "user_id")
		self.assertTrue(finergy.db.exists("User", user))

		new_patient = finergy.get_doc(
			{
				"doctype": "Patient",
				"first_name": "_Test Patient Duplicate User",
				"sex": "Male",
				"email": "test-patient-user@example.com",
				"mobile": "+91 0000000009",
				"invite_user": 1,
			}
		)

		self.assertRaises(finergy.exceptions.DuplicateEntryError, new_patient.insert)
