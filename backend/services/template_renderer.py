from jinja2 import Environment, FileSystemLoader

def render_resume(template_name: str, context: dict):
    env = Environment(loader=FileSystemLoader("backend/templates"))
    template = env.get_template(template_name)
    return template.render(context)