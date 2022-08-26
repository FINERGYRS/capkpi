# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.contacts.address_and_contact import load_address_and_contact
from finergy.utils import get_url
from finergy.website.website_generator import WebsiteGenerator


class GrantApplication(WebsiteGenerator):
	_website = finergy._dict(
		condition_field="published",
	)

	def validate(self):
		if not self.route:  # pylint: disable=E0203
			self.route = "grant-application/" + self.scrub(self.name)

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def get_context(self, context):
		context.no_cache = True
		context.show_sidebar = True
		context.parents = [
			dict(label="View All Grant Applications", route="grant-application", title="View Grants")
		]


def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.no_breadcrumbs = True
	context.show_sidebar = True
	context.order_by = "creation desc"
	context.introduction = """<a class="btn btn-primary" href="/my-grant?new=1">
		Apply for new Grant Application</a>"""


@finergy.whitelist()
def send_grant_review_emails(grant_application):
	grant = finergy.get_doc("Grant Application", grant_application)
	url = get_url("grant-application/{0}".format(grant_application))
	finergy.sendmail(
		recipients=grant.assessment_manager,
		sender=finergy.session.user,
		subject="Grant Application for {0}".format(grant.applicant_name),
		message="<p> Please Review this grant application</p><br>" + url,
		reference_doctype=grant.doctype,
		reference_name=grant.name,
	)

	grant.status = "In Progress"
	grant.email_notification_sent = 1
	grant.save()
	finergy.db.commit()

	finergy.msgprint(_("Review Invitation Sent"))
