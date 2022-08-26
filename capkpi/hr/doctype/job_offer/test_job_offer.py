# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors and Contributors
# See license.txt

import unittest

import finergy
from finergy.utils import add_days, nowdate

from capkpi.hr.doctype.designation.test_designation import create_designation
from capkpi.hr.doctype.job_applicant.test_job_applicant import create_job_applicant
from capkpi.hr.doctype.staffing_plan.test_staffing_plan import make_company

# test_records = finergy.get_test_records('Job Offer')


class TestJobOffer(unittest.TestCase):
	def test_job_offer_creation_against_vacancies(self):
		finergy.db.set_value("HR Settings", None, "check_vacancies", 1)
		job_applicant = create_job_applicant(email_id="test_job_offer@example.com")
		job_offer = create_job_offer(job_applicant=job_applicant.name, designation="UX Designer")

		create_staffing_plan(
			name="Test No Vacancies",
			staffing_details=[
				{"designation": "UX Designer", "vacancies": 0, "estimated_cost_per_position": 5000}
			],
		)
		self.assertRaises(finergy.ValidationError, job_offer.submit)

		# test creation of job offer when vacancies are not present
		finergy.db.set_value("HR Settings", None, "check_vacancies", 0)
		job_offer.submit()
		self.assertTrue(finergy.db.exists("Job Offer", job_offer.name))

	def test_job_applicant_update(self):
		finergy.db.set_value("HR Settings", None, "check_vacancies", 0)
		create_staffing_plan()
		job_applicant = create_job_applicant(email_id="test_job_applicants@example.com")
		job_offer = create_job_offer(job_applicant=job_applicant.name)
		job_offer.submit()
		job_applicant.reload()
		self.assertEqual(job_applicant.status, "Accepted")

		# status update after rejection
		job_offer.status = "Rejected"
		job_offer.submit()
		job_applicant.reload()
		self.assertEquals(job_applicant.status, "Rejected")
		finergy.db.set_value("HR Settings", None, "check_vacancies", 1)

	def tearDown(self):
		finergy.db.sql("DELETE FROM `tabJob Offer` WHERE 1")


def create_job_offer(**args):
	args = finergy._dict(args)
	if not args.job_applicant:
		job_applicant = create_job_applicant()

	if not finergy.db.exists("Designation", args.designation):
		designation = create_designation(designation_name=args.designation)

	job_offer = finergy.get_doc(
		{
			"doctype": "Job Offer",
			"job_applicant": args.job_applicant or job_applicant.name,
			"offer_date": args.offer_date or nowdate(),
			"designation": args.designation or "Researcher",
			"status": args.status or "Accepted",
		}
	)
	return job_offer


def create_staffing_plan(**args):
	args = finergy._dict(args)
	make_company()
	finergy.db.set_value("Company", "_Test Company", "is_group", 1)
	if finergy.db.exists("Staffing Plan", args.name or "Test"):
		return
	staffing_plan = finergy.get_doc(
		{
			"doctype": "Staffing Plan",
			"name": args.name or "Test",
			"from_date": args.from_date or nowdate(),
			"to_date": args.to_date or add_days(nowdate(), 10),
			"staffing_details": args.staffing_details
			or [{"designation": "Researcher", "vacancies": 1, "estimated_cost_per_position": 50000}],
		}
	)
	staffing_plan.insert()
	staffing_plan.submit()
	return staffing_plan
