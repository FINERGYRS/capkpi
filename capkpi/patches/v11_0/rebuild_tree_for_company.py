import finergy
from finergy.utils.nestedset import rebuild_tree


def execute():
	finergy.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company", "parent_company")
