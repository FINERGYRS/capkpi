import finergy
from finergy.utils.verified_command import verify_request


@finergy.whitelist(allow_guest=True)
def get_context(context):
	if not verify_request():
		context.success = False
		return context

	email = finergy.form_dict["email"]
	appointment_name = finergy.form_dict["appointment"]

	if email and appointment_name:
		appointment = finergy.get_doc("Appointment", appointment_name)
		appointment.set_verified(email)
		context.success = True
		return context
	else:
		context.success = False
		return context
