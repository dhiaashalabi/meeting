import frappe
from frappe import _
from frappe.utils import add_days, nowdate

@frappe.whitelist()
def send_invitation_emails(meeting):
    meeting = frappe.get_doc("Meeting", meeting)
    meeting.check_permission("email")
    if meeting.status == "Planned":
        frappe.sendmail(
            recipients=[d.attendee for d in meeting.attendee],
            sender=frappe.session.user,
            subject=meeting.subject,
            message=meeting.invitation_message,
            reference_doctype=meeting.doctype,
            reference_name=meeting.name,
        )
        
        meeting.status = "In progress"
        meeting.save()
        frappe.msgprint(_("Invitation Sent"))
    else:
        frappe.msgprint(_("Meeting status must be Planning to send invitations"))

@frappe.whitelist()
def get_meetings(start, end):
    frappe.msgprint("get_meetings")
    if not frappe.has_permission("Meeting", "read"):
        raise frappe.PermissionError
    return frappe.db.sql(
        """Select 
        timestamp(`date`, from_time) as start,
        timestamp(`date`, to_time) as end,
        name,
        subject,
        status
        from `tabMeeting`
        where `date` between %(start)s and %(end)s""",
        { "start": start, "end": end}, as_dict=True
    )

@frappe.whitelist()
def make_orientation_meeting(doc, method):
    meeting = frappe.get_doc({
        "doctype": "Meeting",
        "subject": "Orientation for {}".format(doc.first_name),
        "date": add_days(nowdate(), 1),
        "from_time": "10:00",
        "to_time": "11:00",
        "status": "Planned",
        "attendee": [{
            "attendee": doc.name
        }]
    })
    meeting.insert(ignore_permissions=True)

def update_meeting_status(doc, method):
    if doc.reference_type != "Meeting" or doc.flags.from_meeting:
        return
    if method  == "on_trash" or doc.status == "Closed":
        meeting = frappe.get_doc(doc.reference_type, doc.reference_name)
        for minute in meeting.minutes:
            if minute.todo == doc.name:
                minute.db_set("todo", None, update_modified=False)
                minute.db_set("status", "Closed", update_modified=False)
        frappe.db.set_value("Meeting", doc.reference_name, "status", "Cancelled")