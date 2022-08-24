# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy
from finergy.utils import random_string

# test_records = finergy.get_test_records('Vehicle')


class TestVehicle(unittest.TestCase):
	def test_make_vehicle(self):
		vehicle = finergy.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": finergy.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": finergy.utils.flt(500000),
			}
		)
		vehicle.insert()
