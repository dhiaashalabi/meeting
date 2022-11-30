# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Meeting(Document):
	def validate(self):
		found = []
		for attendee in self.attendee:
			if not attendee.full_name:
				user = frappe.get_doc("User", attendee.attendee)
				attendee.full_name = user.full_name
			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} is added twice".format(attendee.attendee)))
			found.append(attendee.attendee)

@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))