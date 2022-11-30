frappe.listview_settings["Meeting"] = {
    get_indicator: function(doc) {
        return[__(doc.status), {
            "Planned": "blue",
            "In Progress": "red",
            "Completed": "green",
            "Canceled": "darkgrey"
        }[doc.status], "status,=,"+ doc.status]
    }
}