# Copyright (c) 2022, Frappe and Contributors
# See license.txt

import frappe
import unittest

class TestMeeting(unittest.TestCase):
	def test_sync_todo(self):
		meeting = make_meeting()
		todos = get_todos(meeting)
		self.assertEqual(todos[0].name, meeting.minutes[0].todo)
		self.assertEqual(todos[0].description, meeting.minutes[0].discussion)

	def test_sync_todos_removed(self):
		meeting = make_meeting()
		meeting.minutes[0].status = "Closed"
		meeting.save()

		todos = get_todos(meeting)
		self.assertEqual(len(todos), 0)

	def test_sync_todos_on_close_todo(self):
		meeting = make_meeting()
		todos = get_todos(meeting)
		todo = frappe.get_doc("ToDo", todos[0].name)
		todo.status = "Closed"
		todo.save()
		meeting.reload()
		self.assertEqual(meeting.minutes[0].status, "Closed")
		self.assertFalse(meeting.minutes[0].todo)

def make_meeting():
    meeting = frappe.get_doc({
			"doctype": "Meeting",
			"subject": "_Test Meeting",
			"status": "Planned",
			"date": "2022-01-01",
			"from_time": "10:00",
			"to_time": "11:00",
			"minutes": [
				{
					"discussion": "Test Minute 1",
					"status": "Open",
					"assigned_to": "test@example.com",
				}
			]
		})
    meeting.insert()
    return meeting

def get_todos(meeting):
    return frappe.get_all("ToDo", 
			filters={
				"reference_type": meeting.doctype, 
				"reference_name": meeting.name,
				"owner": "test@example.com"
				},
			fields=["name", "description"]
		)