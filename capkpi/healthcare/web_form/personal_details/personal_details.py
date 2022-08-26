import finergy
from finergy import _

no_cache = 1


def get_context(context):
	if finergy.session.user == "Guest":
		finergy.throw(_("You need to be logged in to access this page"), finergy.PermissionError)

	context.show_sidebar = True

	if finergy.db.exists("Patient", {"email": finergy.session.user}):
		patient = finergy.get_doc("Patient", {"email": finergy.session.user})
		context.doc = patient
		finergy.form_dict.new = 0
		finergy.form_dict.name = patient.name


def get_patient():
	return finergy.get_value("Patient", {"email": finergy.session.user}, "name")


def has_website_permission(doc, ptype, user, verbose=False):
	if doc.name == get_patient():
		return True
	else:
		return False
