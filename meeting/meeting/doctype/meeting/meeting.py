# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Meeting(Document):
	def validate(self):
		# found = []
		# for attendee in self.attendee:
		# 	if not attendee.full_name:
		# 		user = frappe.get_doc("User", attendee.attendee)
		# 		attendee.full_name = user.full_name
		# 	if attendee.attendee in found:
		# 		frappe.throw(_("Attendee {0} is added twice".format(attendee.attendee)))
		# 	found.append(attendee.attendee)
		# self.sync_todo()
		self.validate_attendee()

	def on_update(self):
		self.sync_todo()

	def validate_attendee(self):
		found = []
		for attendee in self.attendee:
			if not attendee.full_name:
				user = frappe.get_doc("User", attendee.attendee)
				attendee.full_name = user.full_name
			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} is added twice".format(attendee.attendee)))
			found.append(attendee.attendee)

	def sync_todo(self):
		todos_added = [todo.name for todo in
                frappe.get_all("ToDo",
                    filters={
						"reference_type": self.doctype,
						"reference_name": self.name,
						"assigned_by": ""
					})
		]
		for minute in self.minutes:
			if minute.assigned_to and minute.status == "Open":
				if not minute.todo:
					todo = frappe.get_doc({
						"doctype": "ToDo",
						"description": minute.discussion,
						"reference_type": self.doctype,
						"reference_name": self.name,
						"owner": minute.assigned_to,
					})
					todo.insert()
					minute.todo = todo.name
				else:
					todos_added.remove(minute.todo)
			else:
				minute.db_set("todo", None, update_modified=False)
		for todo in todos_added:
			todo = frappe.get_doc("ToDo", todo)
			todo.flags.from_meeting = True
			todo.delete()

@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))