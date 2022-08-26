# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors and Contributors
# See license.txt

import unittest

import finergy

from capkpi.hr.doctype.designation.test_designation import create_designation


class TestJobApplicant(unittest.TestCase):
	def test_job_applicant_naming(self):
		applicant = finergy.get_doc(
			{
				"doctype": "Job Applicant",
				"status": "Open",
				"applicant_name": "_Test Applicant",
				"email_id": "job_applicant_naming@example.com",
			}
		).insert()
		self.assertEqual(applicant.name, "job_applicant_naming@example.com")

		applicant = finergy.get_doc(
			{
				"doctype": "Job Applicant",
				"status": "Open",
				"applicant_name": "_Test Applicant",
				"email_id": "job_applicant_naming@example.com",
			}
		).insert()
		self.assertEqual(applicant.name, "job_applicant_naming@example.com-1")

	def tearDown(self):
		finergy.db.rollback()


def create_job_applicant(**args):
	args = finergy._dict(args)

	filters = {
		"applicant_name": args.applicant_name or "_Test Applicant",
		"email_id": args.email_id or "test_applicant@example.com",
	}

	if finergy.db.exists("Job Applicant", filters):
		return finergy.get_doc("Job Applicant", filters)

	job_applicant = finergy.get_doc(
		{
			"doctype": "Job Applicant",
			"status": args.status or "Open",
			"designation": create_designation().name,
		}
	)

	job_applicant.update(filters)
	job_applicant.save()

	return job_applicant
