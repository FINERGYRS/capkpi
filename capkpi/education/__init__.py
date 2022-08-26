import finergy
from finergy import _


class StudentNotInGroupError(finergy.ValidationError):
	pass


def validate_student_belongs_to_group(student, student_group):
	groups = finergy.db.get_all("Student Group Student", ["parent"], dict(student=student, active=1))
	if not student_group in [d.parent for d in groups]:
		finergy.throw(
			_("Student {0} does not belong to group {1}").format(
				finergy.bold(student), finergy.bold(student_group)
			),
			StudentNotInGroupError,
		)
