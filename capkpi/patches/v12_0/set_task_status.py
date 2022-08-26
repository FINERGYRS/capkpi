import finergy


def execute():
	finergy.reload_doctype("Task")

	# add "Completed" if customized
	property_setter_name = finergy.db.exists(
		"Property Setter", dict(doc_type="Task", field_name="status", property="options")
	)
	if property_setter_name:
		property_setter = finergy.get_doc("Property Setter", property_setter_name)
		if not "Completed" in property_setter.value:
			property_setter.value = property_setter.value + "\nCompleted"
			property_setter.save()

	# renamed default status to Completed as status "Closed" is ambiguous
	finergy.db.sql('update tabTask set status = "Completed" where status = "Closed"')
