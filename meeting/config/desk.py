from frappe import _

def get_data():
	return [
		{
            "label": _("Tools"),
			"icon": "octicon octicon-file-directory",
            "items": [
                {
                    "type": "doctype",
                    "name": "Meeting",
                    "label": _("Meeting"),
                    "description": _("Meeting"),
                }
            ],
		}
	]
