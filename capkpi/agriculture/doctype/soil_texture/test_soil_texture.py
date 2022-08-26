# Copyright (c) 2017, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestSoilTexture(unittest.TestCase):
	def test_texture_selection(self):
		soil_tex = finergy.get_all(
			"Soil Texture", fields=["name"], filters={"collection_datetime": "2017-11-08"}
		)
		doc = finergy.get_doc("Soil Texture", soil_tex[0].name)
		self.assertEqual(doc.silt_composition, 50)
		self.assertEqual(doc.soil_type, "Silt Loam")
