finergy.provide("education");

cur_frm.add_fetch("student_group", "course", "course")
finergy.ui.form.on("Course Schedule", {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Mark Attendance"), function() {
				finergy.route_options = {
					based_on: "Course Schedule",
					course_schedule: frm.doc.name
				}
				finergy.set_route("Form", "Student Attendance Tool");
			}).addClass("btn-primary");
		}
	}
});
