# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import today


class LeaveType(Document):
	def validate(self):
		if self.is_lwp:
			leave_allocation = finergy.get_all(
				"Leave Allocation",
				filters={"leave_type": self.name, "from_date": ("<=", today()), "to_date": (">=", today())},
				fields=["name"],
			)
			leave_allocation = [l["name"] for l in leave_allocation]
			if leave_allocation:
				finergy.throw(
					_(
						"Leave application is linked with leave allocations {0}. Leave application cannot be set as leave without pay"
					).format(", ".join(leave_allocation))
				)  # nosec

		if self.is_lwp and self.is_ppl:
			finergy.throw(_("Leave Type can be either without pay or partial pay"))

		if self.is_ppl and (
			self.fraction_of_daily_salary_per_leave < 0 or self.fraction_of_daily_salary_per_leave > 1
		):
			finergy.throw(_("The fraction of Daily Salary per Leave should be between 0 and 1"))
