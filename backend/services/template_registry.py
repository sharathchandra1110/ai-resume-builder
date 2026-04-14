TEMPLATES = [
    {
        "id": "ats_single_column",
        "name": "Professional Blue - Single Column",
        "description": "Sample-inspired one-column resume with clean section dividers",
        "file_name": "ats_single_column.html",
    },
    {
        "id": "modern_two_column",
        "name": "Modern - Two Column",
        "description": "Two-column layout with a skills sidebar and project-focused main panel",
        "file_name": "modern_two_column.html",
    },
]

_TEMPLATE_INDEX = {template["id"]: template for template in TEMPLATES}


def get_template(template_id: str):
    return _TEMPLATE_INDEX.get(template_id)
