import finergy

import capkpi.education.utils as utils

no_cache = 1


def get_context(context):
	if finergy.session.user == "Guest":
		finergy.local.flags.redirect_location = "/lms"
		raise finergy.Redirect

	context.student = utils.get_current_student()
	if not context.student:
		context.student = finergy.get_doc("User", finergy.session.user)
	context.progress = get_program_progress(context.student.name)


def get_program_progress(student):
	enrolled_programs = finergy.get_all(
		"Program Enrollment", filters={"student": student}, fields=["program"]
	)
	student_progress = []
	for list_item in enrolled_programs:
		program = finergy.get_doc("Program", list_item.program)
		progress = utils.get_program_progress(program)
		completion = utils.get_program_completion(program)
		student_progress.append(
			{
				"program": program.program_name,
				"name": program.name,
				"progress": progress,
				"completion": completion,
			}
		)

	return student_progress
