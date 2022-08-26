// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

if(!window.capkpi) window.capkpi = {};

// Add / update a new Lead / Communication
// subject, sender, description
finergy.send_message = function(opts, btn) {
	return finergy.call({
		type: "POST",
		method: "capkpi.templates.utils.send_message",
		btn: btn,
		args: opts,
		callback: opts.callback
	});
};

capkpi.subscribe_to_newsletter = function(opts, btn) {
	return finergy.call({
		type: "POST",
		method: "finergy.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: {"email": opts.email},
		callback: opts.callback
	});
}

// for backward compatibility
capkpi.send_message = finergy.send_message;
