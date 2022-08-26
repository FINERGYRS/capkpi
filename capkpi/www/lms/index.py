import finergy

import capkpi.education.utils as utils

no_cache = 1


def get_context(context):
	context.education_settings = finergy.get_single("Education Settings")
	if not context.education_settings.enable_lms:
		finergy.local.flags.redirect_location = "/"
		raise finergy.Redirect
	context.featured_programs = get_featured_programs()


def get_featured_programs():
	return utils.get_portal_programs() or []
