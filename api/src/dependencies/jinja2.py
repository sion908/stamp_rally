from fastapi.templating import Jinja2Templates

from setting import base_url, stage_name

templates = Jinja2Templates(directory="templates")

def global_context_processor():
    return {
        'base_url': base_url,
        'stage_name': stage_name,
    }

templates.env.globals.update(global_context_processor())
