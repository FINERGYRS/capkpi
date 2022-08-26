# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import flt


class VehicleLog(Document):
	def validate(self):
		if flt(self.odometer) < flt(self.last_odometer):
			finergy.throw(
				_("Current Odometer Value should be greater than Last Odometer Value {0}").format(
					self.last_odometer
				)
			)

	def on_submit(self):
		finergy.db.set_value("Vehicle", self.license_plate, "last_odometer", self.odometer)

	def on_cancel(self):
		distance_travelled = self.odometer - self.last_odometer
		if distance_travelled > 0:
			updated_odometer_value = (
				int(finergy.db.get_value("Vehicle", self.license_plate, "last_odometer")) - distance_travelled
			)
			finergy.db.set_value("Vehicle", self.license_plate, "last_odometer", updated_odometer_value)


@finergy.whitelist()
def make_expense_claim(docname):
	expense_claim = finergy.db.exists("Expense Claim", {"vehicle_log": docname})
	if expense_claim:
		finergy.throw(_("Expense Claim {0} already exists for the Vehicle Log").format(expense_claim))

	vehicle_log = finergy.get_doc("Vehicle Log", docname)
	service_expense = sum([flt(d.expense_amount) for d in vehicle_log.service_detail])

	claim_amount = service_expense + (flt(vehicle_log.price) * flt(vehicle_log.fuel_qty) or 1)
	if not claim_amount:
		finergy.throw(_("No additional expenses has been added"))

	exp_claim = finergy.new_doc("Expense Claim")
	exp_claim.employee = vehicle_log.employee
	exp_claim.vehicle_log = vehicle_log.name
	exp_claim.remark = _("Expense Claim for Vehicle Log {0}").format(vehicle_log.name)
	exp_claim.append(
		"expenses",
		{"expense_date": vehicle_log.date, "description": _("Vehicle Expenses"), "amount": claim_amount},
	)
	return exp_claim.as_dict()
