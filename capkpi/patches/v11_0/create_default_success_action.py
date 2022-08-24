import finergy

from capkpi.setup.install import create_default_success_action


def execute():
	finergy.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
