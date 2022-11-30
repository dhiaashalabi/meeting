frappe.views.calender["Meeting"] = {
    field_map: {
        "start": "from_date",
        "end": "to_date",
        "id": "name",
        "title": "subject",
        "status": "status",
    },
    options:{
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month'
        },
        get_events_method: "meeting.api.get_meetings",
    }
}