# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy.model.document import Document


class InterviewRound(Document):
	pass


@finergy.whitelist()
def create_interview(doc):
	if isinstance(doc, str):
		doc = json.loads(doc)
		doc = finergy.get_doc(doc)

	interview = finergy.new_doc("Interview")
	interview.interview_round = doc.name
	interview.designation = doc.designation

	if doc.interviewers:
		interview.interview_details = []
		for data in doc.interviewers:
			interview.append("interview_details", {"interviewer": data.user})
	return interview
